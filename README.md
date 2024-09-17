# Byte_2_Clean

**Byte_2_Clean** is a Python-based tool designed to help you efficiently find and delete duplicate files from an external drive or a specified directory. It provides both secure and fast options for hashing, while saving and restoring progress in case the process is interrupted.

## Features:
- **Hash-based Duplicate Detection**: Detects duplicate files using either SHA-256 (secure) or XXHash (fast).
- **Progress Save/Restore**: Automatically saves progress in a `progress.json` file and resumes scanning from the last completed file if interrupted.
- **Multi-threading Support**: Scans multiple files in parallel for improved performance.
- **Manual/Automatic Deletion**: Option to either confirm deletions manually or automatically delete duplicates.
- **Real-time Progress Feedback**: Provides progress updates via a `tqdm` progress bar.

## Setup Instructions:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/4lp1ne/Byte_2_Clean.git
   cd Byte_2_Clean
   ```

2. **Set up a virtual environment (optional but recommended)**:
   - **For Linux/Mac**:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - **For Windows**:
     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage:

Run the script to start scanning for duplicates:

```bash
python byte_2_clean.py
```

- **Step 1**: The script will prompt you to enter the directory path to scan for duplicates.
- **Step 2**: Select the hashing strategy:
  - `1` for **secure** (SHA-256)
  - `2` for **fast** (XXHash)
- **Step 3**: After scanning, you can choose to manually confirm deletions or automatically delete all duplicates.

## Example Project Structure:
```
Byte_2_Clean/
│
├── byte_2_clean.py        # Main script
├── progress.json          # Generated file for saving progress
├── README.md              # Documentation
└── requirements.txt       # Dependencies (tqdm, xxhash)
```

## Future Enhancements:
- Add multi-threading improvements for larger directories.
- Support for more hashing algorithms (e.g., SHA-256, xxhash64).
- More detailed duplicate reporting with file metadata.
