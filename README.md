<p align="center">
<img width="100%" src="docs/readme-header.png"><br/><br/>
    <a href="https://www.python.org/downloads/release/python-381/" alt="Activity">
        <img src="https://img.shields.io/badge/Python-3.8.1%20(x64)-blue?style=flat&labelColor=3776AB&color=3776AB&logo=python&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Javascript-6-blue?style=flat&labelColor=F7DF1E&color=F7DF1E&logo=javascript&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Windows-10-blue?style=flat&labelColor=0078D6&color=0078D6&logo=windows&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/MacOS-10.14-blue?style=flat&labelColor=999999&color=999999&logo=apple&logoColor=white" /></a>
    </br>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Office-365-blue?style=flat&labelColor=E74025&color=E74025&logo=microsoft-office&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Chrome-80-blue?style=flat&labelColor=EDAD00&color=EDAD00&logo=google-chrome&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Firefox-72-blue?style=flat&labelColor=FF7139&color=FF7139&logo=mozilla-firefox&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Edge-80-blue?style=flat&labelColor=0078D7&color=0078D7&logo=microsoft-edge&logoColor=white" /></a>
    <a href="#computerlogger" alt="Activity">
        <img src="https://img.shields.io/badge/Opera-66-blue?style=flat&labelColor=FF1B2D&color=FF1B2D&logo=opera&logoColor=white" /></a> <br/><br/>
  <img width="80%" src="docs/gui.jpg"/>

</p>

## Installation and execution:

You must use _64bit_ version of Python 3. (Tested on _Python 3.8.1 64bit_)

#### 1. **Install dependencies**

-   Install project dependencies

    ```bash
    pip3 install -r requirements.txt
    ```

-   Install RPA dependencies

    [Details here](https://github.com/marco2012/ComputerLogger#rpa)

#### 2. **Install browser extension**

The browser extension supports 4 major browsers (<a href="https://gs.statcounter.com/browser-market-share/desktop/" target="_blank">80% market share combined</a>).

-   [_Google Chrome_](https://www.google.com/chrome/): load unpacked `browserlogger` directory in `chrome://extensions/`

-   [_Mozilla Firefox_](https://www.mozilla.org/en-US/firefox/new/): load unpacked `browserlogger` directory in `about:debugging#/runtime/this-firefox`

-   [_Microsoft Edge (chromium)_](https://www.microsoft.com/en-us/edge): load unpacked `browserlogger` directory in `edge://extensions/`

-   [_Opera_](https://www.opera.com/): load unpacked `browserlogger` directory in `opera:extensions`

Once main logger is running, **you must click** on the browser extension to enable it.

#### 3. **Install Excel Addin (MacOS Only)**

The excel addin is required to enable logging <u>only on MacOS</u>.

[`NodeJS`](https://nodejs.org/en/download/) must be installed to run this addin.

```bash
cd modules/excelAddinMac
npm install
npm start
```

Once installed, choose the `Home` tab in Excel, and then choose the `Show Taskpane` button in the ribbon to open the add-in task pane.

#### 4. **Run main logger**

```bash
python3 mainLogger.py
```

The resulting log csv file will be in `/logs` directory.

## RPA

_Robotic Process Automation_ scripts are automatically generated for each log in `/RPA` directory

#### Automagica

To run the generated RPA scripts you must install `automagica` module.

- On Windows:

    1. Make sure you are using <a href="https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe">64bit version of Python3</a>
    2. Install <a href="https://slproweb.com/download/Win64OpenSSL-1_1_1d.exe">Win64 OpenSSL v1.1.1d</a>
    3. Open CMD as <i>admin</i> and type:

    ```cmd
    set LIB=C:\Program Files\OpenSSL-Win64\lib;%LIB%
    set INCLUDE=C:\Program Files\OpenSSL-Win64\include;%INCLUDE%
    pip3 install automagica==2.0.25
    ```

- On MacOS:

    ```bash
    pip3 install automagica==2.0.25
    python3 utils/fix_automagica_permissions.py
    ```

#### PM4PY

To enable process discovery techniques you must install [PM4PY](https://pm4py.fit.fraunhofer.de/features) python module.

- On Windows:

    1. Install a Windows C/C++ compiler like [MinGW](https://osdn.net/projects/mingw/releases/) or [Visual Studio](https://visualstudio.microsoft.com/en/thank-you-downloading-visual-studio/?sku=Community&rel=15)
    2. Install [graphviz-2.38.msi](https://graphviz.gitlab.io/_pages/Download/windows/graphviz-2.38.msi)
    3. Add `C:/Program Files/Graphviz/bin` folder to [system path](https://stackoverflow.com/a/44272417/1440037)
    4. `pip3 install pm4py==1.2.12 pm4pybpmn==0.1.3` 

    </br>
    <details>
    <summary>
        Click to show how to <b>fix installation errors</b> on Windows
    </summary>
    </br>

    If you get the error <code>ERROR: Could not find a version that satisfies the requirement ortools</code> make sure you are using <a href="https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe">64bit version of Python3</a>. 

    </details>

- On MacOS:
    ```bash
    brew install graphviz
    pip3 install pm4py==1.2.12 pm4pybpmn==0.1.3
    ```

#### Browser automation

For browser automation, [Google Chrome](https://www.google.com/chrome/) must be installed.


## Modules

The project is composed by the following modules:

-   [x] GUI
-   [x] CSV server logger
-   [x] System logger
-   [x] Browser logger
-   [x] Office logger
-   [x] Clipboard logger
-   [x] RPA module
-   [x] CSV to XES converter
-   [x] Process Mining analysis

A complete list of features for each module is available in [`features.pdf`](https://github.com/marco2012/ComputerLogger/blob/master/docs/Features.pdf)
