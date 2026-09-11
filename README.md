# DICOM Upload Preparer

DICOM Upload Preparer analyzes a DICOM study, groups images into clearly identified series, and prepares ZIP archives that are easier to review, transfer, or upload.

It can also create anonymized copies of the DICOM files before they are prepared for sharing.

> [!IMPORTANT]
> This tool helps organize DICOM files. It does **not** determine which images a doctor, radiologist, hospital, or upload portal requires. Always follow the receiving institution's instructions when they ask for a complete study or specific series.

# Can I run it on my computer?

Yes, on most normal desktop and laptop computers.

| Computer / operating system | Supported? | Notes |
|---|---:|---|
| Windows 10 / 11 PC | ✅ Yes | Python 3 is required |
| Mac with Apple Silicon (M1/M2/M3/M4...) | ✅ Yes | Python 3 is required |
| Intel Mac | ✅ Yes | Python 3 is required |
| Linux desktop/laptop | ✅ Yes | Python 3, `pydicom`, and `tkinter` are required for the graphical interface |
| Raspberry Pi with desktop Linux | ✅ Should work | Suitable if Python 3 and `tkinter` are installed; processing large studies can be slower |
| Linux server without a graphical desktop | ⚠️ Command line only | Use `prepare-dicom-upload` instead of the GUI |
| Chromebook | ⚠️ Possible with Linux enabled | Not intended as a primary supported setup |
| iPhone / iPad | ❌ No | This is a desktop Python application |
| Android phone/tablet | ❌ No | This is a desktop Python application |
| Web browser only | ❌ No | The application runs locally on your computer |

The program does not require a powerful graphics card or GPU. Processing speed mainly depends on the number and size of the DICOM files and the speed of your storage.

> [!NOTE]
> There is not yet a standalone Windows `.exe` or macOS `.app`. In the current version, Python must be installed once before using the graphical interface.

# I know almost nothing about computers — how do I use it?

This section is for users who normally download a program, open it, select a folder, and click a button.

You do **not** need to understand DICOM, Python programming, Terminal commands, or how the files are classified.

## Step 1 — Download DICOM Upload Preparer

1. Open this GitHub repository in your web browser.
2. Click the green **Code** button near the top of the page.
3. Click **Download ZIP**.
4. When the download finishes, open your **Downloads** folder.
5. Extract/unzip the downloaded ZIP file.

You should now have a folder named something similar to:

```text
dicom-upload-preparer-main
```

Do not run the program directly from inside the downloaded ZIP archive. Extract it first.

## Step 2 — Install Python

You only need to do this once.

### Windows 10 / Windows 11

1. Go to https://www.python.org/downloads/
2. Download the current Python 3 installer for Windows.
3. Run the installer.
4. On the first installation screen, enable **Add python.exe to PATH** if that option is shown.
5. Complete the installation.

To check that Python is installed:

1. press the **Windows** key;
2. type `PowerShell`;
3. open **Windows PowerShell**;
4. type:

```powershell
python --version
```

You should see a Python 3 version number.

### macOS

1. Go to https://www.python.org/downloads/macos/
2. Download and install the current Python 3 installer for macOS.
3. Complete the installation normally.

To check that Python is installed:

1. open **Terminal** (Applications → Utilities → Terminal);
2. type:

```bash
python3 --version
```

You should see a Python 3 version number.

### Linux

Python 3 is already installed on many Linux distributions.

On Debian, Ubuntu, Linux Mint, Raspberry Pi OS, and similar systems, you can install the required components with:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk
```

## Step 3 — Install the DICOM component

The application needs the Python package `pydicom` to read DICOM files. The repository currently requires `pydicom>=3.0`.

### Windows

Open PowerShell and type:

```powershell
python -m pip install pydicom
```

### macOS / Linux

Open Terminal and type:

```bash
python3 -m pip install pydicom
```

If your operating system refuses to install packages globally, use the advanced virtual-environment instructions further below.

## Step 4 — Start the graphical interface

Open the extracted `dicom-upload-preparer-main` folder.

The file that starts the graphical version is:

```text
dicom-upload-preparer-gui.py
```

### Windows

The most reliable method is:

1. open the extracted `dicom-upload-preparer-main` folder in File Explorer;
2. click the address bar at the top of File Explorer;
3. type `powershell` and press **Enter**;
4. in the PowerShell window that opens, type:

```powershell
python dicom-upload-preparer-gui.py
```

A window called **DICOM Upload Preparer** should appear.

### macOS

1. Open **Terminal**.
2. Type `cd `, including the space after `cd`.
3. Drag the extracted `dicom-upload-preparer-main` folder from Finder into the Terminal window. macOS will insert the folder path automatically.
4. Press **Enter**.
5. Type:

```bash
python3 dicom-upload-preparer-gui.py
```

A window called **DICOM Upload Preparer** should appear.

### Linux

Open a terminal in the extracted repository folder and run:

```bash
python3 dicom-upload-preparer-gui.py
```

## Step 5 — Choose your DICOM examination

In the DICOM Upload Preparer window:

1. Next to **DICOM source folder**, click **Browse…**.
2. Select the folder containing your medical DICOM examination.

This can be, for example:

- a folder copied from a CD/DVD supplied by a hospital;
- a folder copied from a USB drive;
- an examination downloaded from a medical portal;
- a folder containing many `.dcm` files;
- a folder containing subfolders with DICOM files.

You do **not** need to manually find each individual DICOM series. Select the main folder containing the examination.

## Step 6 — Choose where the prepared files will be created

The GUI proposes an output folder named:

```text
dicom-prepared
```

You can keep this default or click **Browse…** to choose another location.

> [!IMPORTANT]
> Do not put the output folder inside the original DICOM source folder. The graphical interface checks this to avoid accidentally processing its own generated files.

## Step 7 — Decide whether to anonymize the files

The option **Anonymize DICOM files before writing them** is enabled by default.

Leave it enabled if you want the prepared copies to have common direct patient identifiers removed or replaced before sharing them.

The program also removes private DICOM tags. DICOM UIDs are preserved so that relationships between image series and objects such as RTSTRUCT, SEG, and SR remain usable.

> [!WARNING]
> Anonymization reduces exposure of common identifiers, but no automated anonymization process should be treated as a guarantee that a medical file contains no identifying information. Follow the requirements of the doctor, hospital, research project, or upload service receiving the files.

## Step 8 — ZIP options

For most users, leave **Create ZIP archives** enabled.

The default maximum ZIP size is:

```text
430 MB
```

If a DICOM series is larger than this limit, the program automatically creates several ZIP files such as:

```text
004_FLAIR_..._part01.zip
004_FLAIR_..._part02.zip
```

You normally do not need to change this setting unless the website receiving the files has a different upload-size limit.

## Step 9 — Click “Prepare DICOM files”

Click:

**Prepare DICOM files**

The application will:

1. scan the selected folder;
2. detect DICOM files;
3. group them into DICOM series;
4. classify and prioritize the detected series;
5. copy the series into organized folders;
6. anonymize the copies if requested;
7. create ZIP archives if requested;
8. generate a summary and a detailed inventory.

The log area at the bottom of the window shows what the program is doing.

Do not close the application while processing is running.

## Step 10 — Open the result

When processing is finished, use the button to open the output folder.

You will normally see:

```text
dicom-prepared/
├── README.txt
├── manifest.tsv
├── series/
└── zip/
```

For a non-technical user, only two things are initially important:

| What you want to do | Open this |
|---|---|
| Understand what the program found | `README.txt` |
| Find the ZIP files to upload or transfer | `zip/` |

### Start with `README.txt`

`README.txt` is a human-readable summary of the examination.

It shows the detected series and places higher-priority series first.

### Need to upload files?

Open:

```text
zip/
```

The ZIP archives in this directory are the prepared files intended for transfer or upload.

If a hospital or doctor specifically asks for the **complete examination**, do not send only the priority series: follow their instructions and provide everything they request.

# Troubleshooting for beginners

## “python is not recognized” on Windows

Python is either not installed or Windows cannot find it.

Reinstall Python from python.org and enable **Add python.exe to PATH** during installation.

Then close PowerShell, reopen it, and try:

```powershell
python --version
```

## “No module named pydicom”

Install `pydicom`.

Windows:

```powershell
python -m pip install pydicom
```

macOS / Linux:

```bash
python3 -m pip install pydicom
```

## “No module named tkinter” or the GUI does not open on Linux

Install Tkinter.

On Debian, Ubuntu, Linux Mint, Raspberry Pi OS, and similar systems:

```bash
sudo apt install python3-tk
```

## The program finds no DICOM series

Make sure you selected the main folder containing the actual medical examination rather than an unrelated folder.

DICOM media can contain several levels of subfolders. The program searches recursively, so you normally only need to select the top-level examination folder.

## Can I modify my original medical files by mistake?

The program reads from the source folder and creates prepared copies in the output folder. It does not intentionally modify the source DICOM files.

# I am comfortable with computers or the command line

The command-line version provides direct access to the same DICOM preparation engine.

## Requirements

- Python 3
- `pydicom>=3.0`
- `tkinter` only if using the graphical interface

Clone the repository:

```bash
git clone https://github.com/jplacq/dicom-upload-preparer.git
cd dicom-upload-preparer
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the GUI:

```bash
python dicom-upload-preparer-gui.py
```

On systems where the Python executable is named `python3`:

```bash
python3 dicom-upload-preparer-gui.py
```

Display the available command-line options:

```bash
python3 prepare-dicom-upload --help
```

A typical command is:

```bash
python3 prepare-dicom-upload "/path/to/dicom-study" -o "dicom-prepared" --anonymize
```

To change the maximum size of each ZIP archive:

```bash
python3 prepare-dicom-upload "/path/to/dicom-study" -o "dicom-prepared" --max-zip-mb 430
```

To prepare the series without creating ZIP files:

```bash
python3 prepare-dicom-upload "/path/to/dicom-study" -o "dicom-prepared" --no-zip
```

> [!NOTE]
> Keep the output directory outside the source DICOM directory. This prevents previously generated files from being scanned again if the tool is run a second time.

# What does the tool create?

| File / directory | Typical user | Purpose |
|---|---|---|
| `README.txt` | Everyone | Quick human-readable summary of the processed study |
| `zip/` | Everyone | ZIP archives intended for upload or transfer |
| `manifest.tsv` | Advanced users | Detailed structured inventory of detected DICOM series |
| `series/` | Advanced users | Prepared individual DICOM files grouped by series |

If you are unsure where to start, open **`README.txt` first**.

# Output details

The tool creates an output directory with the following structure:

```text
dicom-prepared/
├── README.txt
├── manifest.tsv
├── series/
└── zip/
```

## `manifest.tsv`

`manifest.tsv` is a tab-separated inventory of all DICOM series detected in the input study.

Each row represents one DICOM series and includes, when available:

- computed priority;
- detected series class, for example `DWI`, `ADC`, `T2`, `CT_THORAX_C_THIN`, `RTSTRUCT`;
- DICOM modality, such as `MR`, `CT`, `RTSTRUCT` or `SR`;
- anatomical plane: `AXIAL`, `CORONAL`, `SAGITTAL` or `UNKNOWN`;
- DICOM series number;
- series description;
- protocol name;
- body part examined;
- slice thickness;
- CT reconstruction kernel;
- contrast agent information;
- number of images in the series;
- total series size;
- image dimensions;
- generated directory name under `series/`;
- generated ZIP archive name or names under `zip/`.

Because it is a TSV file, it can be opened directly in spreadsheet applications such as Microsoft Excel, LibreOffice Calc, Numbers, or parsed with standard command-line and scripting tools.

## `README.txt`

`README.txt` is a human-readable summary generated for the specific DICOM study that was processed.

It contains:

- the original source directory;
- the total number of detected series;
- whether anonymization was enabled;
- a priority-series section containing the series considered most useful for review;
- an other-series section for the remaining acquisitions;
- for each listed series, its detected class, anatomical plane, series number, description, image count, approximate size, and corresponding ZIP archive name.

This file is intended to be the quickest way to decide which series should be reviewed or shared first without opening every DICOM series individually.

## `series/`

The `series/` directory contains the prepared DICOM files grouped into one subdirectory per detected DICOM series.

For example:

```text
series/
├── 001_DWI_AXIAL_S4_Ax_DWI_Muse_b1000_...
├── 002_ADC_AXIAL_S450_ADC_...
├── 003_T2_AXIAL_S5_Ax_T2_brain_...
└── ...
```

Inside each series directory, the DICOM objects are renamed sequentially:

```text
000001.dcm
000002.dcm
000003.dcm
...
```

The ordering is derived, when possible, from DICOM metadata rather than from the original filenames. The script uses anatomical position, instance number, and temporal/acquisition position to produce a consistent ordering.

When `--anonymize` is used, the DICOM files stored in `series/` are the anonymized copies produced by the tool. Private DICOM tags are removed and common direct patient identifiers are cleared or replaced.

The `series/` directory is mainly useful for local inspection, importing into a DICOM viewer, further processing, or verifying the generated data before sharing it.

## `zip/`

The `zip/` directory contains archives ready for upload, transfer, or review.

Normally, one ZIP archive is generated for each DICOM series:

```text
zip/
├── 001_DWI_AXIAL_S4_Ax_DWI_Muse_b1000_....zip
├── 002_ADC_AXIAL_S450_ADC_....zip
├── 003_T2_AXIAL_S5_Ax_T2_brain_....zip
└── ...
```

Each archive contains the same prepared DICOM files found in the corresponding subdirectory under `series/`.

If a single series exceeds the size configured with `--max-zip-mb`, the series is automatically split into multiple archives, for example:

```text
004_FLAIR_..._part01.zip
004_FLAIR_..._part02.zip
```

This makes large studies easier to upload through services that impose per-file size limits.

In practice:

- use `README.txt` to decide what to review or send first;
- use `manifest.tsv` for a complete structured inventory;
- use `series/` for local DICOM inspection and processing;
- use `zip/` for sharing or uploading selected series.
