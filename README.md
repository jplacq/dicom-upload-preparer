## Output

The tool creates an output directory with the following structure:

    dicom-prepared/
    ├── README.txt
    ├── manifest.tsv
    ├── series/
    └── zip/

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
- a `PRIORITY SERIES` section containing the series considered most useful for review;
- an `OTHER SERIES` section for the remaining acquisitions;
- for each listed series, its detected class, anatomical plane, series number, description, image count, approximate size, and corresponding ZIP archive name.

This file is intended to be the quickest way to decide which series should be reviewed or shared first without opening every DICOM series individually.

### `series/`

The `series/` directory contains the prepared DICOM files grouped into one subdirectory per detected DICOM series.

For example:

    series/
    ├── 001_DWI_AXIAL_S4_Ax_DWI_Muse_b1000_...
    ├── 002_ADC_AXIAL_S450_ADC_...
    ├── 003_T2_AXIAL_S5_Ax_T2_brain_...
    └── ...

Inside each series directory, the DICOM objects are renamed sequentially:

    000001.dcm
    000002.dcm
    000003.dcm
    ...

The ordering is derived, when possible, from DICOM metadata rather than from the original filenames. The script uses anatomical position, instance number, and temporal/acquisition position to produce a consistent ordering.

When `--anonymize` is used, the DICOM files stored in `series/` are the anonymized copies produced by the tool. Private DICOM tags are removed and common direct patient identifiers are cleared or replaced.

The `series/` directory is mainly useful for local inspection, importing into a DICOM viewer, further processing, or verifying the generated data before sharing it.

### `zip/`

The `zip/` directory contains archives ready for upload, transfer, or review.

Normally, one ZIP archive is generated for each DICOM series:

    zip/
    ├── 001_DWI_AXIAL_S4_Ax_DWI_Muse_b1000_....zip
    ├── 002_ADC_AXIAL_S450_ADC_....zip
    ├── 003_T2_AXIAL_S5_Ax_T2_brain_....zip
    └── ...

Each archive contains the same prepared DICOM files found in the corresponding subdirectory under `series/`.

If a single series exceeds the size configured with `--max-zip-mb`, the series is automatically split into multiple archives, for example:

    004_FLAIR_..._part01.zip
    004_FLAIR_..._part02.zip

This makes large studies easier to upload through services that impose per-file size limits.

In practice:

- use `README.txt` to decide what to review or send first;
- use `manifest.tsv` for a complete structured inventory;
- use `series/` for local DICOM inspection and processing;
- use `zip/` for sharing or uploading selected series.
