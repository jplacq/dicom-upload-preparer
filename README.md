# DICOM Upload Preparer

DICOM Upload Preparer analyzes a DICOM study, groups images into clearly identified series, and prepares ZIP archives that are easier to review, transfer, or upload.

It can also create anonymized copies of the DICOM files before they are prepared for sharing.

> [!IMPORTANT]
> This tool helps organize DICOM files. It does **not** determine which images a doctor, radiologist, hospital, or upload portal requires. Always follow the receiving institution's instructions when they ask for a complete study or specific series.

## Which instructions should I follow?

There are two ways to use DICOM Upload Preparer.

### 🖱️ I just want to click and use it

Choose this option if you normally use applications by opening them, selecting files or folders, and clicking buttons.

The graphical interface lets you:

1. choose the folder containing your DICOM examination;
2. choose where the prepared files will be created;
3. choose whether the DICOM files should be anonymized;
4. choose the maximum ZIP size;
5. click **Prepare DICOM files**;
6. open the generated output folder when processing is finished.

Start the graphical interface with:

```bash
python3 dicom-upload-preparer-gui.py
```

On Windows, depending on your Python installation, use:

```powershell
python dicom-upload-preparer-gui.py
```

The graphical interface uses only Python's standard GUI toolkit (`tkinter`). The DICOM processing itself requires `pydicom`.

After processing, open the generated output directory. The GUI suggests a `dicom-prepared` directory next to the selected DICOM source folder.

Inside it, start with:

```text
dicom-prepared/
├── README.txt       ← start here
├── manifest.tsv     ← complete technical inventory
├── series/          ← prepared DICOM series
└── zip/             ← ZIP files ready for upload
```

If you only want to know what to send or review first, open **`README.txt`**.

For files intended for upload or transfer, open the **`zip/`** directory.

#### Privacy

Medical DICOM files can contain personal information.

If **Anonymize DICOM files** is enabled, DICOM Upload Preparer creates anonymized copies, removes private DICOM tags, and clears or replaces common direct patient identifiers.

UIDs are preserved so that relationships between objects such as RTSTRUCT, SEG, SR, and image series remain usable.

Anonymization is intended to reduce exposure of common patient identifiers, but you should still follow the data-protection and submission requirements of the receiving institution.

---

### 💻 I am comfortable with computers or the command line

Choose this option if you are familiar with Terminal, PowerShell, Python, virtual environments, or shell commands.

DICOM Upload Preparer is a Python command-line utility.

#### Requirements

- Python 3
- `pydicom`

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

## What does the tool create?

| File / directory | Typical user | Purpose |
|---|---|---|
| `README.txt` | Everyone | Quick human-readable summary of the processed study |
| `zip/` | Everyone | ZIP archives intended for upload or transfer |
| `manifest.tsv` | Advanced users | Detailed structured inventory of detected DICOM series |
| `series/` | Advanced users | Prepared individual DICOM files grouped by series |

If you are unsure where to start, open **`README.txt` first**.

## Output

The tool creates an output directory with the following structure:

```text
dicom-prepared/
├── README.txt
├── manifest.tsv
├── series/
└── zip/
```

### `manifest.tsv`

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

### `README.txt`

`README.txt` is a human-readable summary generated for the specific DICOM study that was processed.

It contains:

- the original source directory;
- the total number of detected series;
- whether anonymization was enabled;
- a priority-series section containing the series considered most useful for review;
- an other-series section for the remaining acquisitions;
- for each listed series, its detected class, anatomical plane, series number, description, image count, approximate size, and corresponding ZIP archive name.

This file is intended to be the quickest way to decide which series should be reviewed or shared first without opening every DICOM series individually.

### `series/`

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

### `zip/`

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
