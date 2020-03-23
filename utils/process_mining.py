# ******************************
# Process mining techniques
# https://pm4py.fit.fraunhofer.de/documentation#discovery
# ******************************
try:
    import ntpath
except ModuleNotFoundError:
    import os
import os
from threading import Thread
import pandas
import utils.config
import utils.utils
from fuzzywuzzy import fuzz
from datetime import datetime

try:
    # constants
    from pm4py.util import constants
    from pm4py.util import xes_constants as xes_util
    # importer
    from pm4py.objects.log.adapters.pandas import csv_import_adapter
    from pm4py.objects.log.importer.xes import factory as xes_importer
    from pm4py.objects.log.exporter.xes import factory as xes_exporter
    from pm4py.objects.conversion.log import factory as conversion_factory
    from pm4py.objects.petri.exporter import pnml as pnml_exporter
    # algorithms
    from pm4py.algo.discovery.alpha import factory as alpha_miner
    from pm4py.algo.discovery.heuristics import factory as heuristics_miner
    from pm4py.algo.discovery.dfg import factory as dfg_factory
    from pm4py.objects.conversion.dfg import factory as dfg_conv_factory
    from pm4py.algo.discovery.inductive import factory as inductive_miner
    # visualization
    from pm4py.visualization.petrinet import factory as vis_factory
    from pm4py.visualization.heuristics_net import factory as hn_vis_factory
    from pm4py.visualization.petrinet import factory as pn_vis_factory
    from pm4py.visualization.dfg import factory as dfg_vis_factory
    from pm4py.objects.log.util import sorting
    from pm4pybpmn.visualization.bpmn import factory as bpmn_vis_factory
    # BPMN
    from pm4pybpmn.objects.conversion.petri_to_bpmn import factory as bpmn_converter
    from pm4pybpmn.objects.bpmn.util import bpmn_diagram_layouter
except ImportError as e:
    print("[PROCESS MINING] Process mining analysis has been disabled because 'pm4py' module is not installed."
          "See https://github.com/marco2012/ComputerLogger#PM4PY")


class ProcessMining:

    def __init__(self, filepath: list):

        # list of csv paths
        self.filepath = filepath
        # last csv in the list, use its name
        self.last_csv = self.filepath[-1]
        # name and extension of the last csv in the list
        self.filename = utils.utils.getFilename(self.last_csv).strip('_combined')
        self.file_extension = utils.utils.getFileExtension(self.last_csv)
        # path to save generated files, like /Users/marco/ComputerLogger/RPA/2020-03-06_12-50-28/
        self._create_directories()
        self._log = self._handle_log()
        self.mostFrequentCase = self.selectMostFrequentCase()

    def _create_directories(self):
        # create directory if does not exists
        self.save_path = utils.utils.getRPADirectory(self.filename)
        utils.utils.createDirectory(self.save_path)

        self.RPA_log_path = os.path.join(self.save_path, 'log')
        utils.utils.createDirectory(self.RPA_log_path)

        self.discovery_log_path = os.path.join(self.save_path, 'discovery')
        utils.utils.createDirectory(self.discovery_log_path)

    def _handle_log(self):

        if self.file_extension == ".csv":

            # combine multiple csv into one and then export it to xes
            csv_to_combine = list()
            for i, csv_path in enumerate(self.filepath):
                # load csv in pandas dataframe, rename columns to match xes standard and replace null values with
                # empty string
                df = pandas.read_csv(csv_path, encoding='utf-8-sig') \
                    .rename(columns={'event_type': 'concept:name',
                                     'timestamp': 'time:timestamp',
                                     'user': 'org:resource'}) \
                    .fillna('')
                # Each csv should have a separate case ID, so I insert a column to the left of each csv and assign
                # number i. When I convert the combined csv to xes, all the rows with the same number will belong to a
                # single trace, so I will have i traces.

                try:  # insert this column to create a unique trace for each csv
                    df.insert(0, 'case:concept:name', i)
                except ValueError:  # column already present
                    pass

                try:  # insert this column to create a unique trace for each csv
                    df.insert(1, 'case:creator', 'CSV2XES by marco2012')
                except ValueError:  # column already present
                    pass

                try:
                    df.insert(2, 'lifecycle:transition', 'complete')
                except ValueError:
                    pass

                csv_to_combine.append(df)

            # dataframe of combined csv
            combined_csv = pandas.concat(csv_to_combine)

            # insert index for each row
            # combined_csv.insert(0, 'row_index', range(0, len(combined_csv)))

            self.dataframe = combined_csv

            # calculate csv path
            combined_csv_path = os.path.join(self.RPA_log_path, f'{self.filename}_combined.csv')

            # save dataframe as csv
            combined_csv.to_csv(combined_csv_path, index=False, encoding='utf-8-sig')

            # convert csv to xes
            log = conversion_factory.apply(combined_csv)

            # sort by timestamp
            log = sorting.sort_timestamp(log)

            # convert csv to xes
            xes_path = os.path.join(self.save_path, 'log', f'{self.filename}.xes')
            xes_exporter.export_log(log, xes_path)
            print(f"[PROCESS MINING] Generated XES file in {self.save_path}")

            return log

        elif self.file_extension == ".xes":
            log = xes_importer.import_log(self.filepath)
            return log
        else:
            return "[PROCESS_MINING] Input file must be either .csv or .xes"

    # return most frequent case in log in order to build RPA script
    def selectMostFrequentCaseWithoutDuration(self, flattened=False):
        df = self.dataframe
        if df.empty:
            return None

        # flattening
        df['browser_url_hostname'] = df['browser_url'].apply(lambda url: utils.utils.getHostname(url))
        df['flattened'] = df[
            ['concept:name', 'category', 'application', 'browser_url_hostname', "workbook", "cell_content",
             "cell_range", "cell_range_number", "slides"]].agg(','.join, axis=1)
        groupby_column = 'flattened' if flattened else 'concept:name'

        # Merge rows of each trace into one row, so the resulting dataframe has n rows where n is the number of traces
        # For example I get
        # ID  Trace   Action
        # 0   1   Create Fine, Send Fine
        # 1   2   Insert Fine Notification, Add penalty, Payment
        df1 = df.groupby('case:concept:name')[groupby_column].agg(', '.join).reset_index()

        # calculate variants, grouping the previous dataframe
        # concept:name  variants
        # typed, clickTextField, changeField, mouseClick...	    [0]
        # typed, changeField, mouseClick, formSubmit, li...	    [1]
        df2 = df1.groupby(groupby_column, sort=False)['case:concept:name'].agg(list).reset_index(name='variants')

        # get variants as list, each item represents a trace in the log
        # [[0], [1], [2], [3], [4,5]]
        variants = df2['variants'].tolist()

        # longest variant is selected because it's the most frequent
        longest_variants = max(variants, key=len)

        if len(longest_variants) == 1:
            # all the variants contain one case, need to check similarities

            # Check similarities between all the strings in the log and return the most frequent one
            def func(name, threshold=85):
                matches = df2.apply(lambda row: (fuzz.partial_ratio(row[groupby_column], name) >= threshold), axis=1)
                return [i for i, x in enumerate(matches) if x]
            df3 = df2.apply(lambda row: func(row[groupby_column]), axis=1)  # axis=1 means apply function to each row

            # In this example, elements 2 and 4 in variants list are similar to element 0 and so on
            # [[0, 2, 4], [1], [0, 2], [3], [0, 4]]
            match_id_list = df3.tolist()

            # longest variant is selected because it's the most frequent
            longest_variants = max(match_id_list, key=len)
            longest_variant = longest_variants[0]

            if len(longest_variants) == 1:
                print(f"[PROCESS MINING] There is 1 variant, selecting first case")
            else:
                print(f"[PROCESS MINING] There are {len(variants)} variants available, all with 1 case. "
                      f"Variants {list(map(lambda x: x+1, longest_variants))} are similar, "
                      f"selecting the first case of variant {longest_variant+1}")
        else:
            # there is a frequent variant, pick first case
            print(
                f"[PROCESS MINING] There are {len(variants)} variants available, "
                f"the most frequent one contains {len(longest_variants)} cases, selecting the first case")
            longest_variant = longest_variants[0]

        # return rows corresponding to selected trace
        case = df.loc[df['case:concept:name'] == longest_variant]

        return case

    def selectMostFrequentCase(self, flattened=False):
        df = self.dataframe
        if df.empty:
            return None

        # flattening
        df['browser_url_hostname'] = df['browser_url'].apply(lambda url: utils.utils.getHostname(url))
        df['flattened'] = df[
            ['concept:name', 'category', 'application', 'browser_url_hostname', "workbook", "cell_content",
             "cell_range", "cell_range_number", "slides"]].agg(','.join, axis=1)
        groupby_column = 'flattened' if flattened else 'concept:name'

        # Merge rows of each trace into one row, so the resulting dataframe has n rows where n is the number of traces
        # For example I get
        # case:concept:name     concept:name                            timestamp
        # 0                     Create Fine, Send Fine                  2020-03-20 17:09:06:308, 2020-03-20 17:09:06:3
        # 1                     Insert Fine Notification, Add penalty   2020-03-20 17:10:28:348, 2020-03-20 17:10:28:2
        df1 = df.groupby(['case:concept:name'])[[groupby_column, 'time:timestamp']].agg(', '.join).reset_index()

        # calculate duration in seconds for each row of dataframe
        # I get a new a new column like
        # duration
        # 25.123
        # 26.342
        # 22.324
        def getDuration(time):
            timestamps = time.split(',')
            start = datetime.strptime(timestamps[0].strip(), "%Y-%m-%d %H:%M:%S:%f")
            finish = datetime.strptime(timestamps[-1].strip(), "%Y-%m-%d %H:%M:%S:%f")
            duration = finish - start
            return duration.total_seconds()
        df1['duration'] = df1['time:timestamp'].apply(lambda time: getDuration(time))

        # calculate variants, grouping the previous dataframe if there are equal rows
        # concept:name                                          variants   duration
        # typed, clickTextField, changeField, mouseClick...	    [0, 1]    [25.123, 26.342]
        # typed, changeField, mouseClick, formSubmit, li...	    [2]       [22.324]
        df2 = df1.groupby([groupby_column], sort=False)[['case:concept:name', 'duration']].agg(
            list).reset_index().rename(columns={"case:concept:name": "variants"})

        # return the concept:case:id of the variant with shortest duration
        # not used when all traces are different
        def _findVariantWithShortestDuration(df1: pandas.DataFrame, most_frequent_variants):
            #  there are at least 2 equal variants, most_frequent_variants is an array like [0,1]
            # take only the most frequent rows in dataframe, like [0,1]
            most_frequent_variants_df = df1.iloc[most_frequent_variants, :]
            # find the row with the smallest duration
            durations = most_frequent_variants_df['duration'].tolist()
            # return the index of the row with the smallest duration
            min_duration_trace = most_frequent_variants_df.loc[most_frequent_variants_df['duration'] == min(durations)][
                'case:concept:name'].tolist()[0]
            return min_duration_trace, min(durations)

        # get variants as list, each item represents a trace in the log
        # [[0, 1], [2]]
        variants = df2['variants'].tolist()

        # longest variant is selected because it's the most frequent
        # [0, 1]
        most_frequent_variants = max(variants, key=len)

        if len(most_frequent_variants) == 1:
            # all variants are different, I need to check similarities or find the one with the
            # shortest duration in the whole dataset

            # Check similarities between all the strings in the log and return the most frequent one
            #  I don't need to check similarities in the other case, because there the strings are exactly the same
            def func(name, threshold=85):
                matches = df2.apply(lambda row: (fuzz.partial_ratio(row[groupby_column], name) >= threshold), axis=1)
                return [i for i, x in enumerate(matches) if x]
            df3 = df2.apply(lambda row: func(row[groupby_column]), axis=1)  # axis=1 means apply function to each row

            most_frequent_variants = max(df3.tolist(), key=len)
            if len(most_frequent_variants) == 1:
                # there are no similar strings, all are different, so I find the one with the smallest duration
                # in the whole dataset, I don't need to filter like in the other cases

                #  get all durations as list
                durations = df1['duration'].tolist()
                #  find smallest duration and select row in dataframe with that duration
                min_duration_trace = df1.loc[df1['duration'] == min(durations)]['case:concept:name'].tolist()[0]

                print(
                    f"[PROCESS MINING] All {len(variants)} variants are different, "
                    f"case {min_duration_trace} is the shortest ({min(durations)} sec)")
            else:
                # some strings are similar, it should be like case below
                min_duration_trace, duration = _findVariantWithShortestDuration(df1, most_frequent_variants)
                print(
                    f"[PROCESS MINING] Traces {most_frequent_variants} are similar, "
                    f"case {min_duration_trace} is the shortest ({duration} sec)")
        else:
            min_duration_trace, duration = _findVariantWithShortestDuration(df1, most_frequent_variants)
            print(
                f"[PROCESS MINING] Traces {most_frequent_variants} are equal, "
                f"case {min_duration_trace} is the shortest ({duration} sec)")

        case = df.loc[df['case:concept:name'] == min_duration_trace]

        return case

    def _create_image(self, gviz, img_name, verbose=False):
        img_path = os.path.join(self.save_path, self.discovery_log_path, f'{self.filename}_{img_name}.pdf')
        if img_name == "alpha_miner":
            vis_factory.save(gviz, img_path)
        elif img_name == "heuristic_miner":
            hn_vis_factory.save(gviz, img_path)
        elif "petri_net" in img_name:
            pn_vis_factory.save(gviz, img_path)
        elif img_name == "DFG":
            dfg_vis_factory.save(gviz, img_path)
        elif "BPMN" in img_name:
            bpmn_vis_factory.save(gviz, img_path)

        if verbose:
            print(f"[PROCESS MINING] Generated {img_name} in {img_path}")

    def create_alpha_miner(self):
        net, initial_marking, final_marking = alpha_miner.apply(self._log)
        gviz = vis_factory.apply(net, initial_marking, final_marking, parameters={"format": "pdf"})
        self._create_image(gviz, "alpha_miner")

    def create_heuristics_miner(self):
        heu_net = heuristics_miner.apply_heu(self._log, parameters={"dependency_thresh": 0.99})
        gviz = hn_vis_factory.apply(heu_net, parameters={"format": "pdf"})
        self._create_image(gviz, "heuristic_miner")

    def _getSourceTargetNodes(self, log=None, high_level=False):
        # source and target nodes in dfg graph are the first and last line in log file
        if log and high_level:
            events_list = [event["customClassifier"] for trace in log for event in trace]
        else:
            events_list = self.dataframe['concept:name'].tolist()
            events_list = [value for value in events_list if value != 'enableBrowserExtension']
        source = events_list[0]
        target = events_list[-1]
        return source, target

    def _createImageParameters(self, log=None, high_level=False):
        source, target = self._getSourceTargetNodes(log, high_level)
        parameters = {"start_activities": [source], "end_activities": [target], "format": "pdf"}
        return parameters

    def _createDFG(self, log=None, parameters=None):
        if parameters is None:
            parameters = {}
        if log is None:
            log = self._log
        dfg = dfg_factory.apply(log, variant="frequency", parameters=parameters)
        return dfg

    # def _createCustomDFG(self):
    #     window = 1
    #     for trace in self._log:
    #         for event in trace:
    #             event["customClassifier"] = f'{event["concept:name"]}-{event["row_index"]}'
    #
    #     parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "customClassifier"}
    #     if constants.PARAMETER_CONSTANT_ACTIVITY_KEY not in parameters:
    #         parameters[constants.PARAMETER_CONSTANT_ACTIVITY_KEY] = xes_util.DEFAULT_NAME_KEY
    #     activity_key = parameters[constants.PARAMETER_CONSTANT_ACTIVITY_KEY]
    #     # dfgs = map((lambda t: [(t[i - window][activity_key], t[i][activity_key]) for i in range(window, len(t))]), log)
    #     dfgs = list()
    #     for t in self._log:
    #         for i in range(window, len(t)):
    #             dfgs.append([(t[i - window][activity_key], t[i][activity_key])])
    #     l_id = list()
    #     for lista in dfgs:
    #         for dfg in lista:
    #             l_id.append(dfg)
    #     counter_id = Counter(l_id)
    #     return counter_id
    #
    # def mostFrequentPathInDFG(self):
    #     dfg = self._createCustomDFG()
    #     source, target = self._getSourceTargetNodes()
    #     graphPath = utils.graphPath.HandleGraph(dfg, source, target)
    #     graphPath.printPath()
    #     return graphPath.frequentPath()
    #

    def save_dfg(self):
        dfg = self._createDFG()
        parameters = self._createImageParameters()
        gviz = dfg_vis_factory.apply(dfg, log=self._log, variant="frequency", parameters=parameters)
        self._create_image(gviz, "DFG")

    @staticmethod
    def _getHighLevelEvent(row):

        e = row["concept:name"]
        url = utils.utils.getHostname(row['browser_url'])
        app = row['application']
        cb = utils.utils.removeWhitespaces(row['clipboard_content'])

        # general
        if e in ["copy", "cut", "paste"]:  # take only first 15 characters of clipboard
            if len(cb) > 20:
                return f"Copy and Paste: {cb[:20]}..."
            if len(cb) == 0:
                return f"Copy and Paste"
            else:
                return f"Copy and Paste: {cb}"

        # browser
        elif e in ["clickButton", "clickTextField", "doubleClick", "clickTextField", "mouseClick", "clickCheckboxButton"]:
            if row['tag_type'] == 'submit':
                return f"[{app}] Submit {row['tag_category'].lower()} on {url}"
            else:
                return f"[{app}] Click {row['tag_type']} {row['tag_category'].lower()} '{row['tag_name']}' on {url}"
        elif e in ["clickLink"]:
            return f"[{app}] Click '{row['tag_innerText']}' on {url}"
        elif e in ["link", "reload", "generated", "urlHashChange", ]:
                return f"[{app}] Navigate to {url}"
        elif e in ["submit", "formSubmit", "selectOptions"]:
            return "Submit"
        elif e in ["selectTab", "moveTab", "zoomTab"]:
            return "Browser Tab"
        elif e in ["newTab"]:
            return f"[{app}] Open tab"
        elif e in ["closeTab"]:
            return f"[{app}] Close tab"
        elif e in ["newWindow"]:
            return f"[{app}] Open window"
        elif e in ["closeWindow"]:
            return f"[{app}] Close window"
        elif e in ["typed", "selectText", "contextMenu"]:
            return f"[{app}] Edit {row['tag_category']} on {url}"
        elif e in ["changeField"]:
            return f"[{app}] Write '{row['tag_value']}' in {row['tag_type']} {row['tag_category'].lower()} on {url}"

        # system
        elif e in ["itemSelected", "deleted", "moved", "created", "Mount", "Unmount", "openFile", "openFolder"]:
            path = row['event_src_path']
            name, extension = ntpath.splitext(path)
            name = ntpath.basename(path)
            if extension:
                return f"[{app}] Edit file '{name}'"
            else:
                return f"[{app}] Edit folder '{name}'"
        elif e in ["programOpen", "programClose"]:
            return f"Use program '{app.lower()}'"

        # excel win
        elif e in ["newWorkbook", "openWorkbook", "activateWorkbook"]:
            return f"[Excel] Open {row['workbook']}"
        elif e in ["editCellSheet", "getCell", "getRange",
                   "editCell", "editRange", "WorksheetCalculated", "WorksheetFormatChanged"]:
            if row['current_worksheet'] != '':
                # return f"[Excel] Edit Cell {row['cell_range']} on {row['current_worksheet']} with value '{row['cell_content']}'"
                return f"[Excel] Edit Cell on {row['current_worksheet']}"
            else:
                return f"[Excel] Edit Cell"
        elif e in ["addWorksheet", "deselectWorksheet", "selectWorksheet", "WorksheetActivated"]:
            return f"[Excel] Select {row['current_worksheet']}"

        # powerpoint
        elif e in ["newPresentation"]:
            return f"[PowerPoint] Open {row['title']}"
        elif e in ["newPresentationSlide", "savePresentation", "SlideSelectionChanged"]:
            return f"[PowerPoint] Edit presentation"

        # word
        elif e in ["newDocument"]:
            return f"[Word] Open document"
        elif e in ["changeDocument"]:
            return f"[Word] Edit document"

        else:
            return e

    def _aggregateData(self, remove_duplicates=False):

        df = self.mostFrequentCase

        # filter rows
        df = df[~df.browser_url.str.contains('chrome-extension://')]
        df = df[~df.eventQual.str.contains('clientRedirect')]
        df = df[~df.eventQual.str.contains('serverRedirect')]
        df = df[df['clipboard_content'].str.strip() == '']
        rows_to_remove = ["activateWindow", "deactivateWindow", "openWindow", "newWindow", "closeWindow",
                          "selectTab", "moveTab", "zoomTab", "typed", "mouseClick", "submit", "formSubmit",
                          "installBrowserExtension", "enableBrowserExtension", "disableBrowserExtension",
                          "resizeWindow", "logonComplete", "startPage", "doubleClickCellWithValue",
                          "doubleClickEmptyCell", "rightClickCellWithValue", "rightClickEmptyCell", "afterCalculate",
                          "programOpen", "programClose", "closePresentation", "SlideSelectionChanged", "closeWorkbook",
                          "deactivateWorkbook", "WorksheetAdded"]
        df = df[~df['concept:name'].isin(rows_to_remove)]

        # convert each row of events to high level
        df['customClassifier'] = df.apply(lambda row: self._getHighLevelEvent(row), axis=1)

        # check duplicates
        # print(df[df['customClassifier'].duplicated() == True])
        # remove duplicates
        if remove_duplicates:
            df = df.drop_duplicates(subset='customClassifier', keep='first')

        log = conversion_factory.apply(df)
        parameters = {constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "customClassifier"}
        return log, parameters

    def _create_petri_net(self, remove_duplicates=False):
        log, dfg_parameters = self._aggregateData(remove_duplicates)
        dfg = self._createDFG(log, dfg_parameters)
        parameters = self._createImageParameters(log=log, high_level=True)
        net, im, fm = dfg_conv_factory.apply(dfg, parameters=parameters)
        return net, im, fm

    def save_petri_net(self, name):
        net, im, fm = self._create_petri_net()
        gviz = pn_vis_factory.apply(net, im, fm, parameters={"format": "pdf"})
        self._create_image(gviz, name)

    def _create_bpmn(self):

        log, parameters = self._aggregateData(remove_duplicates=True)
        net, initial_marking, final_marking = heuristics_miner.apply(log, parameters=parameters)

        #net, initial_marking, final_marking = self._create_petri_net(remove_duplicates=True)

        bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = bpmn_converter.apply(
            net, initial_marking, final_marking)

        # bpmn_graph = bpmn_diagram_layouter.apply(bpmn_graph)

        return bpmn_graph

    def save_bpmn(self):
        bpmn_graph = self._create_bpmn()
        bpmn_figure = bpmn_vis_factory.apply(bpmn_graph, variant="frequency", parameters={"format": "pdf"})
        self._create_image(bpmn_figure, "BPMN")

    def createGraphs(self):
        self.save_dfg()
        self.save_petri_net('petri_net')
        self.save_bpmn()  # includes petri net
        print(f"[PROCESS MINING] Generated DFG, Petri Net and BPMN in {self.discovery_log_path}")
