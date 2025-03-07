<p align="center">
<img width="100%" src="src/images/readme-header.png"><br/><br/>
    <a href="https://www.python.org/downloads/" alt="Activity">
        <img src="https://img.shields.io/badge/Python-3.10 (x64)-blue?style=flat&labelColor=3776AB&color=3776AB&logo=python&logoColor=white" /></a>
    <a href="#" alt="Activity">
        <img src="https://img.shields.io/badge/Javascript-ES6-blue?style=flat&labelColor=F7DF1E&color=F7DF1E&logo=javascript&logoColor=white" /></a>
    <a href="#" alt="Activity">
        <img src="https://img.shields.io/badge/Windows-10/11-blue?style=flat&labelColor=0078D6&color=0078D6&logo=windows&logoColor=white" /></a>
    <a href="#" alt="Activity">
        <img src="https://img.shields.io/badge/MacOS-14-blue?style=flat&labelColor=999999&color=999999&logo=apple&logoColor=white" /></a>
    </br>
    <a href="https://www.office.com/" alt="Activity">
        <img src="https://img.shields.io/badge/Office-365-blue?style=flat&labelColor=E74025&color=E74025&logo=microsoft-office&logoColor=white" /></a>
    <a href="https://www.google.com/chrome/" alt="Activity">
        <img src="https://img.shields.io/badge/Chrome-85-blue?style=flat&labelColor=EDAD00&color=EDAD00&logo=google-chrome&logoColor=white" /></a>
    <a href="https://www.mozilla.org/en-US/firefox" alt="Activity">
        <img src="https://img.shields.io/badge/Firefox-72-blue?style=flat&labelColor=FF7139&color=FF7139&logo=mozilla-firefox&logoColor=white" /></a>
    <a href="https://www.microsoft.com/en-us/edge" alt="Activity">
        <img src="https://img.shields.io/badge/Edge-80-blue?style=flat&labelColor=0078D7&color=0078D7&logo=microsoft-edge&logoColor=white" /></a>
    <a href="https://www.opera.com/" alt="Activity">
        <img src="https://img.shields.io/badge/Opera-66-blue?style=flat&labelColor=FF1B2D&color=FF1B2D&logo=opera&logoColor=white" /></a> 
    <br/>
    <a href="#"><img src="https://img.shields.io/badge/Sapienza University of Rome-blue?style=flat&labelColor=781A2D&color=781A2D&logoColor=white" /></a> 
  <br/><br/>
  <img width="80%" src="src/images/gui.png"/>

</p>

# What is SmartRPA

**Robotic Process Automation (RPA)** is a technology which automates mouse and keyboard interactions by means of a software (SW) robot to remove intensive routines.
The current generation of RPA tools is driven by predefined rules and manual configurations made by expert users rather than automated techniques.

**SmartRPA** is a cross-platform tool that tackles such issues. It allows to easily record event logs and to automatically generating executable RPA scripts that will drive a SW robots in emulating an observed user behavior (previously recorded in dedicated UI logs) during the enactment of a routine of interest.

## Authors

**SmartRPA** has been developed at **DIAG**, Department of Computer, Control, and Management Engineering _Antonio Ruberti_ in **Sapienza University of Rome** by:

- [Simone Agostinelli](https://www.diag.uniroma1.it/users/simone_agostinelli)
- [Marco Lupia](https://marco2012.github.io/)
- [Andrea Marrella](http://www.dis.uniroma1.it/marrella/)

Many thanks also to [Tom Hohenadl](https://www.linkedin.com/in/thohenadl/) (**Technische Hochschule Ingolstadt**) and [Antonio Martínez-Rojas](https://personal.us.es/amrojas/) (**Universidad de Sevilla**) for the ongoing updates of the tool.

<!--The **associated paper** is available on [Springer](https://doi.org/10.1007/978-3-030-58779-6_8), and has been presented at the [RPA Forum](https://congreso.us.es/bpm2020/calls/rpa/) of _18th International Conference on Business Process Management_.-->

A **Screencast** of the tool is available on \[[Vimeo](https://vimeo.com/569988752)\]. Additionally, a dedicated video showcasing both the **screenshot** and **supervision** features is included here \[[Vimeo](https://vimeo.com/1027046243)\].

## Architecture

The architecture of SmartRPA integrates five main SW components.

<p align="center">
  <img width="55%" src="src/images/architecture.jpeg"/>
</p>

**Key features** include:

- [x] **Action Logger**, log user behaviour, take screenshots, tag actions, supports wide range of applications, cross-platform;
- [x] **Log Processing**, generates both CSV and XES event log;
- [x] **Event abstraction**, abstracts events to a higher level;
- [x] **Process Discovery**, selects the most suitable routine variant to automate and generates high-level flowchart diagram, thus skipping completely the manual modeling activity;
- [x] **Decision Points**, discover differencies between multiple traces in a process and build a new routine based on user decisions;
- [x] **RPA**, implements and enacts a SW robot emulating a routine reflecting the observed behavior (either the most frequent one or the one based on decision points). Available both as a cross-platform _Python script_ and as a _UiPath_ project.

A **list of events** supported by the Action Logger is available in [`SmartRPA_events.pdf`](https://github.com/bpm-diag/smartRPA/blob/master/src/images/SmartRPA_events.pdf).

The full **documentation** of the tool is available [here](https://bpm-diag.github.io/smartRPA/).
A **user manual** for SmartRPA is available [in this repository here](src/images/SmartRPA_UserManual.pdf).

# Installation and execution:

The following dependencies are required to enable all functionalities within SmartRPA. Check all boxes and you are able to log user actions, discover process models, and emulate RPA bots in UiPath and Automagica automatically:

- [Prerequisites](#1-install-prerequisites)
  - [Visual Studio C/C++ Build Tools (Windows Only)](#11-visual-studio-windows-only)
  - [Graphviz Windows/Mac](#12a-graphviz-windows)
  - [Automagica](#22-automagica-library)
  - [Chromedriver for Edge/Chrome](#23-chromedriver-required-for-chromeedge-users)
  - [UiPath Studio](#24-uipath-windows-only-optional)
- Action Logger dependencies
  - [Python Requirements](#21-requirementstxt)
  - [Browser extension](#3-install-browser-extension)
- [Excel AddIn (MacOS Only)](#4-install-excel-addin-macos-only)
- [LLM Tagger](#6-llm-based-activity-tagging-beta)

Furthermore, there are possible installation issues that can arise with the installation of the prerequisites or libraries. You can find fixes to the most common issues in the section [Installation Errors](#error-handling-for-possible-installation-errors) .

## 1. **Install Prerequisites**

### 1.1 Visual Studio (Windows Only)

<img width="40%" src="src/images/visual_studio.png">

- On **Windows**, [Visual Studio C/C++ Build Tools](https://visualstudio.microsoft.com/en/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) must be installed.
  It is vital to install all C++ related development tools listed here:

  - Windows 10/11 SDK
  - Visual C++ tools for CMake
  - C++ x64/x86 build tools

  
### 1.2a GraphViz Windows

Install the latest version of [graphviz](https://www2.graphviz.org/Packages/stable/windows/10/cmake/Release/x64/). Make sure to add it to system PATH. Detailed instructions [here](https://forum.graphviz.org/t/new-simplified-installation-procedure-on-windows/224).


### 1.2b GraphViz Mac

- On **MacOS**:

  1. Make sure you installed [brew](https://brew.sh/) package manager
  2. Check [brew] installation for graphviz with `brew install graphviz`
  3. Check pm4py installation and run `pip3 install pm4py==1.5.0.1` if necessary


## 2. **Python Installation**

### 2.1 Requirements.txt

[Python](https://www.python.org/downloads/) ≥ 3.7 (_64bit_) is required. Python 3.12 is recommended.

  ```bash
  pip3 install -r src/requirements.txt
  ```

We have specified three requirements files for distinct Python versions. We recommend using the specified requirements file. The **requirements.txt** is for Python 3.12.

<details>
<summary>
CMD installation lines for Python 3.7 and Python 3.10
</summary>
  <br/>

  ```bash
  pip3 install -r src/requirements308.txt
  ```
  <br/>

  ```bash
  pip3 install -r src/requirements310.txt
  ```
  <br/>
</details>

### 2.2 Automagica Library

To run the generated RPA scripts you must install `automagica` module available in the `libraries` directory.

  ```bash
  pip3 install src/libraries/smartRPA-automagica-2-1-12.zip
  ```

  <details>
  <summary>
  CMD installation lines Automagica with Python <= 3.7
  </summary>
  
  ```bash
  pip3 install src/libraries/Automagica-2.0.25-py3-none-any.whl`
  ```

  </details>

### 2.3 Chromedriver (Required for Chrome/Edge users)

Required for executing the emulated **Automagica Python** bots in Chrome and Edge.
To select the correct version of the pip installation for the Chromedriver go to the Chrome or Edge [settings/help](chrome://settings/help). Get the version number, e.g., Version 124.0.2478.97. Navigate to [PyPi Chromedriver History](https://pypi.org/project/chromedriver-binary/#history). Select the release with a same main number, e.g., chromedriver-binary 124.0.6367.207.0, and install this version using pip, i.e.,

```bash
pip install chromedriver-binary==124.0.6367.207.0
```


### 2.4 UiPath (Windows Only) (Optional)

The generated UiPath project requires _UiPath Studio_, available at [https://www.uipath.com/product/studio](https://www.uipath.com/product/studio). </br>Without UiPath Studio you cannot import and execute the generated UiPath bots from SmartRPA.


## 3. **Install browser extension**

The browser extension is required to log browser events. It is available in `src/extensions/browserlogger` and supports 4 major browsers:

- [_Google Chrome_](https://www.google.com/chrome/): load unpacked `browserlogger` directory in `chrome://extensions/`

- [_Mozilla Firefox_](https://www.mozilla.org/en-US/firefox/new/): install [`browserlogger.xpi`](https://github.com/bpm-diag/smartRPA/blob/develop/extensions/browserlogger/browserlogger.xpi?raw=true) in `about:addons`

- [_Microsoft Edge (chromium)_](https://www.microsoft.com/en-us/edge): load unpacked `browserlogger` directory in `edge://extensions/`

- [_Opera_](https://www.opera.com/): load unpacked `browserlogger` directory in `opera:extensions`

Currently the browser extension **requires the developer mode to be active** in your browser. Please check the browser documentation on how to enable the developer mode.

<details>
<summary>
Enabling the Browser Logger
</summary>

Once the main logger is running, **you must click** on the browser extension to enable it.
</br>

| Inactive Browser Logging  | Active Browser Logging |
| ------------- | ------------- |
| <img width="100%" src="src/images/disabledBrowserLogger.png"/>  | <img width="100%" src="src/images/enabledBrowserLogger.png"/> |

</details>

## 4. Install Excel Addin (MacOS Only)

The excel addin is required to log Excel events <u>only on MacOS</u>.

[`Node.js`](https://nodejs.org/en/download/) must be installed to run this addin.

```bash
cd src/extensions/excelAddinMac
npm install # install dependencies
npm start   # sideload Add-in
npm stop    # stop server
```

<details>
<summary>
    Click to show how to <b>activate the Add-in</b> in Excel
</summary>
</br>

<ol type="a">
  <li>Start the Action Logger selecting Excel module</li>
  <li>Go to <code>Insert</code> tab</li>
  <li>Click on the small down-arrow to the right of <code>My Add-ins</code> > <code>OfficeLogger</code></li>
  <img width="50%" src="src/images/excel_logger.png">
  <li>Go to <code>Home</code> tab</li>
  <li>Click the <code>Show Taskpane</code> button in the ribbon</li>
  <li>Enable the checkbox</li>
</ol>

If you don't find <code>OfficeLogger</code> under <code>My Add-ins</code>, copy <code>extensions/excelAddinMac/manifest.xml</code> into <code>~/Library/Containers/com.microsoft.Excel/Data/Documents/wef</code>, as described <a href="https://docs.microsoft.com/en-us/office/dev/add-ins/testing/sideload-an-office-add-in-on-ipad-and-mac#sideload-an-add-in-in-office-on-mac">here</a>.

</details>

## 5. Run main logger

```bash
python3 main.py
```

A detailed **screencast** of the tool is available on \[[Vimeo](https://vimeo.com/569988752)\] including the core functions of recording, analyzing, and emulating RPA bots.
The resulting event log will be saved in `logs/` directory. If the screenshot feature is active the screenshots are stored in the `Screenshots` directory. 
</br>SmartRPA generates two types of SW Robots in the `RPA/` directory:

1. a cross-platform executable **Python script**, available on both Windows and MacOS
2. a **UiPath project**, available only on Windows

The advantages of the UiPath integration is that the generated SW Robot can be easily customized by the end user.

**NOTE**: In the Action Logger, when selecting a *Microsoft Office* program to log, it will automatically be opened. This is required to correctly handle events. The opened window should not be closed until logging is completed.

## 6. LLM Based Activity Tagging (Beta)
LLMs allow are capable of [Business Process Management tasks](https://link.springer.com/chapter/10.1007/978-3-031-50974-2_34) and therefore can be used to semantically tag data.
We integrated such a feature in the processing menu. 

 - Open the Processing/LLM Tagging Menu
 - Store your Gemini API code. A manual to obtain an Gemini API key is found [here](https://ai.google.dev/gemini-api/docs/api-key).
 - Select the UI log you want to semantically tag
 - Start the promoting to generate short text descriptions of the activities conducted

This feature is currently in Beta as the prompt results sometimes to not contain proper JSON responses for parsing or long logs cannot be processed accuratly.

### Action Logger Only

If you only want the action logger to record event logs without further analysis, you can find it [here](https://github.com/bpm-diag/smartRPA/tree/action_logger) .
Please note that this logger is associated with version 1.0 of SmartRPA and has not been updated with the new functionalities (Supervision Feature, Screenshot Feature, Updated Python Libraries) of SmartRPA 2.0.

## Error Handling for possible installation errors

### 1. Visual Studio Errors

<details>
<summary> 
  Error: Microsoft Visual C++ 14.0 is required
</summary>
  </br>
  If you encounter errors like `Microsoft Visual C++ 14.0 is required`, [check here](https://bobbyhadz.com/blog/error-microsoft-visual-c-14-0-or-greater-is-required) .
</details>

### 2. Graphviz Errors

<details>
<summary>
Windows: Fix <b>graphviz</b> error: Command '[WindowsPath('dot'), '-Kdot', '-Tpdf', '-O', 'tmp24z1pppy.gv']' returned non-zero exit status 1.
</summary>
</br>

```bash
Could not save image: Command '[WindowsPath('dot'), '-Kdot', '-Tpdf', '-O', 'tmp24z1pppy.gv']' returned non-zero exit status 1. [stderr: b'There is no layout engine support for "dot"\r\nPerhaps "dot -c" needs to be run (with installer\'s privileges) to register the plugins?\r\n'] 
```

If you recieve the shown error and you use Anaconda or conda, you have to use another version of the graphviz python library. 
With conda run the following comand in your environment:

```bash
conda install conda-forge::python-graphviz conda-forge::graphviz=2.46.1
```

</details>

<details>
<summary>
    Click to show how to <b>fix</b> <code>ModuleNotFoundError</code> error on Windows
</summary>
</br>

If you have installed all the [requirements](#21-requirementstxt) but you still get <code>ModuleNotFoundError</code>, run SmartRPA with:

```bash
py main.py
```

</details>

<details>
<summary>
    MacOS: Click to show how to <b>fix installation errors</b> on MacOS
</summary>
</br>

If you get an error during installation:

- If you're on **MacOS 10.14 Mojave**, run the following command as suggested [here](https://github.com/python-pillow/Pillow/issues/3438#issuecomment-435169249), and then, in the same terminal window, install `pm4py` again

```bash
sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
```

- If you're on **MacOS 10.15 Catalina**, run the following command as suggested [here](https://github.com/python-pillow/Pillow/issues/3438#issuecomment-543812237), and then, in the same terminal window, install `pm4py` again

```bash
export CPATH=`xcrun --show-sdk-path`/usr/include
```

- If you're on **MacOS 11.0 Big Sur**, install the latest nightly build version of `scikit-learn` running the following command and then install `pm4py` again

```bash
pip3 install --pre --extra-index https://pypi.anaconda.org/scipy-wheels-nightly/simple scikit-learn
```

</details>

### 3. Automagica Errors

<details>
<summary>
    Click to show how to <b>fix installation errors</b> on Windows
</summary>
</br>

1. Make sure you are using <a href="https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe">64bit version of Python3</a>
2. Install `Win64 OpenSSL v1.1.1` from <a href="https://slproweb.com/products/Win32OpenSSL.html">this website</a>. When prompted select _"Copy OpenSSL DLLs to: the Windows system directory"_
3. Open CMD as <i>admin</i> and type (one command per line):

```cmd
set LIB=C:\Program Files\OpenSSL-Win64\lib;%LIB%
set INCLUDE=C:\Program Files\OpenSSL-Win64\include;%INCLUDE%
pip3 install libraries/Automagica-2.0.25-py3-none-any.whl
```
</details>

### 4. Chromedriver Errors

<details>
<summary>
    Click to show how to <b>fix installation errors</b> on MacOS
</summary>
<br>
If you get the error <code>RuntimeError: Failed to download chromedriver archive</code>

1. Navigate to `/Applications/Python 3.x/` folder
2. Run `Install Certificates.command` file
3. Install the package again

<a href="https://stackoverflow.com/a/42107877">Reference</a>

If you don't find the `Python 3.8` folder under `/Applications`, make sure you installed Python using <a href="https://www.python.org/downloads/mac-osx/">the official installer</a> and not from a package manager like brew.

</details>

<details>
<summary>
    Message: session not created: This version of ChromeDriver only supports Chrome version 123
</summary>
<br>
If you get the error <code>Message: session not created: This version of ChromeDriver only supports Chrome version 123</code> when running a smartRPA created bot:

1. Navigate <a href="https://pypi.org/project/chromedriver-binary/#history">Pypi Chromedriver-binary</a>
2. Select the chromedriver-binary matching your current Chrome version. E.g. 121.0.6134.0.0 for Chrome 121
3. Install the package again using the pip command from Pypi, e.g. <code>pip install chromedriver-binary==121.0.6134.0.0</code>

</details>

# Publications

- **Agostinelli S., Lupia M., Marrella A., Mecella M.**: _[Reactive Synthesis of Software Robots in RPA from User Interface Logs](https://doi.org/10.1016/j.compind.2022.103721)_. Accepted at Computers in Industry (Elsevier), 2022
- **Agostinelli, S., Lupia, M., Marrella, A., Mecella, M.**: _[SmartRPA: A Tool to Reactively Synthesize Software Robots from User Interface Logs](https://doi.org/10.1007/978-3-030-79108-7_16)_. In: 33rd Int. Conf. on Advanced Information Systems Engineering (CAiSE Forum). pp. 137-145 (2021)
  - The synthetic UI logs generated for the test are available at: https://tinyurl.com/yyk68psx.
  - The complete results can be analyzed at: https://tinyurl.com/y55v56qa.
- **Agostinelli, S., Lupia, M., Marrella, A., Mecella, M.**: _[Automated Generation of Executable RPA Scripts from User Interface Logs](https://doi.org/10.1007/978-3-030-58779-6_8)_. In: 18th Int. Conf. on Business Process Management (RPA Forum). pp. 116-131 (2020)

# Acknowledgments
This work has been partially supported by the PNRR MUR project PE0000013-FAIR
