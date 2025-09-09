# MDES PDF Editor Project

A lightweight, privacy-focused desktop application built purely in Python for performing essential PDF operations: Merging, Deleting, Extracting, and Splitting.

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Linux](https://img.shields.io/badge/Linux-informational?style=flat&logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

## Why MDES Exists
Working with PDFs shouldn't require uploading sensitive documents to the cloud, installing bloated software, or being limited by your internet bandwidth. MDES provides **(only)** four core PDF operations through a simple, local interface that respects your privacy and guarantees instant efficiency.

## Features
*  🔒 100% Offline & Private: No internet connection needed. Your files never leave your computer.

*  🪶 Ultra Lightweight: Minimal footprint—the application is under 15 MB. Fast performance with no bloat.

*  🛡️ Zero Telemetry: No tracking, analytics, or data collection of any kind.

*  🎯 Simple & Guided UI: A clean, intuitive, and straightforward workflow. No confusing options.

## Core Operations
*  **Merge**: Combine multiple PDF files into a single document.

*  **Split**: Divide a PDF into multiple files by page ranges or at specific page numbers.

*  **Extract**: Pull specific pages or ranges into a new PDF file.

*  **Delete**: Remove unwanted pages from a PDF.

## Installation
**Option 1: Download Executable**
1. Go to the [Releases](../../releases) page.
2. Download the latest MDES PDF Editor.exe file.
3. Run the executable. No installation required.

**Option 2: Run from Source"**
Clone or Package using PyInstaller:
pyinstaller --onefile --windowed --name "MDES_PDF_Editor" gui.py

## How to Use
The workflow is designed to be simple and linear:

1. Select PDF: Choose your input file(s).

2. Choose Folder: Select the destination for the output file.

3. Pick Function: Select your desired operation (Merge, Delete, Extract, or Split).

Configure: Enter the required page numbers or ranges.

Process: Execute the operation.

**That's it!** The status area will display the result of your operation.

**Usage Notes**
*  MERGE: Simply select multiple PDFs. They will be combined in the order you select them.

*  EXTRACT / DELETE: Use comma-separated page numbers and ranges. Example: 1, 3-5, 8 will include pages 1, 3, 4, 5, and 8.

*  SPLIT: Define the page numbers where you want to split the document. Each split point creates a new file. Example: Splitting at pages 5, 9 of a 12-page document will create three files: pages 1-4, 5-8, and 9-12.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
*  Application Icon: Generated using Google Gemini.

*  Development: Built with AI assistance for personal use.

*  Libraries: Powered by the simplicity of Tkinter and the reliability of PyPDF2.

*  README: Drafted with the assistance of Deepseek.

## Disclaimer
This software is provided "as is" for personal purposes. Always verify the results of PDF operations, especially when working with important or sensitive documents.

**Your data stays with you—always offline, always private.**



