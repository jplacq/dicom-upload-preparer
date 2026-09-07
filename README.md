# dicom-upload-preparer

Generic Python tool to identify, classify, anonymize, sort and package DICOM studies for review or sharing.

Supports MRI, CT/TDM and common derived DICOM objects.

## Features

- Recursive DICOM discovery
- MRI sequence classification
- CT/TDM series classification
- Anatomical slice sorting
- DICOM anonymization
- Removal of private DICOM tags
- RTSTRUCT, SEG and SR recognition
- Automatic ZIP packaging
- Automatic splitting of large archives
- TSV manifest generation
- Human-readable series summary

## Requirements

- Python 3
- pydicom

Install dependencies:

    python3 -m pip install -r requirements.txt

## Installation

    chmod +x prepare-dicom-upload
    mkdir -p ~/bin
    cp prepare-dicom-upload ~/bin/

Make sure ~/bin is in your PATH.

For zsh:

    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

## Usage

Basic usage:

    prepare-dicom-upload "/path/to/DICOM"

Recommended usage with anonymization:

    prepare-dicom-upload \
      "/path/to/DICOM" \
      -o ~/Desktop/dicom-prepared \
      --anonymize

Example for MRI:

    prepare-dicom-upload \
      "/Volumes/MRI_EXAM" \
      -o ~/Desktop/mri-prepared \
      --anonymize

Example for CT:

    prepare-dicom-upload \
      "/Volumes/CT_EXAM" \
      -o ~/Desktop/ct-prepared \
      --anonymize

## Output

    dicom-prepared/
    ├── README.txt
    ├── manifest.tsv
    ├── series/
    └── zip/

## Privacy

The --anonymize option removes common direct patient identifiers and private DICOM tags.

DICOM UIDs are deliberately preserved so references between images, RTSTRUCT, SEG and other derived objects remain functional.

Always verify anonymization before publishing medical data publicly.

## Disclaimer

This utility is not a medical device and does not provide medical diagnoses.

## License

MIT
