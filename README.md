# Byte_2_Clean
---
![Screenshot 2024-10-07 043711](https://github.com/user-attachments/assets/b200759b-1237-4205-a6ec-fbee9a50d7ac)
---
### Overview
`Byte_2_Clean` is a Python-based application designed to scan directories for duplicate files using various hashing techniques. The application features an intuitive **graphical user interface (GUI)** built with `tkinter` and supports multiple hashing algorithms to identify and manage duplicates efficiently.

### Features
- **GUI Interface**: User-friendly graphical interface for specifying the directory and choosing the hashing technique.
- **Hashing Techniques**: Supports multiple hashing techniques for scanning efficiency:
  - **SHA-256**: Secure but slower.
  - **xxhash.xxh64**: Faster but less secure.
  - **xxhash.xxh32**: Fastest but least secure.
- **Progress Tracking**: Saves and loads scan progress for efficient processing of large directories.
- **Detailed Logging**: Displays logs and scan results in the GUI to track the process.
- **Delete Functionality**: Option to delete selected duplicates or all duplicates after scanning.

### Recent Modifications
- **Improved GUI Layout**: Adjusted the window size and layout for better usability and visibility.
- **Delete Options**: Added the option to delete all duplicates with a single click, alongside the existing option to delete selected duplicates.
- **Duplicate File Display**: Improved the display of original files and their corresponding duplicates.
- **Open Folder Functionality**: Added the ability to open the folder containing the selected duplicate file.
  
### Installation

#### Prerequisites
- **Python 3.6** or higher.

#### Install Required Packages
To install the required Python packages, run the following command:
```bash
pip install xxhash
```

### Setup

#### Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/4lp1ne/Byte_2_Clean.git
```

#### Navigate to the Project Directory
Change to the project directory:
```bash
cd Byte_2_Clean
```

### Usage

#### Run the Application
Execute the Python script to start the GUI application:
```bash
python duplicate_file_scanner.py
```

#### Using the GUI
1. **Directory Path**: Enter the directory path you want to scan in the input field or use the "Choose Folder" button to select the folder.
2. **Select Hashing Technique**: Choose from the dropdown menu:
   - `"Secure"` for SHA-256 (more secure but slower).
   - `"Thorough"` for xxhash.xxh64 (faster but less secure).
   - `"Quick"` for xxhash.xxh32 (fastest but least secure).
3. **Start Scan**: Click the "Start Scan" button to begin scanning the specified directory.
4. **Display Duplicates**: After scanning, select an original file and click "Display Duplicates of Selected Original" to see the duplicates.
5. **Delete Duplicates**: 
   - Click "Delete Selected Duplicates" to remove only the duplicates you selected from the list.
   - Click "Delete All Duplicates" to remove all detected duplicate files.
6. **Open Folder**: Select a file from the list and click "Open Containing Folder" to open the folder containing that file.
7. **Log Output**: The log area shows detailed information about the scanning and deletion processes.

### Code Description

#### Main Functions
- **save_progress(progress)**: Saves the current scan progress to a JSON file to track scanned files and found duplicates.
- **load_progress()**: Loads scan progress from the JSON file to avoid rescanning files unnecessarily.
- **compute_hash(file_path, hash_func_cls)**: Computes the hash of a file using the selected hashing algorithm.
- **scan_for_duplicates(directory, mode)**: Scans the specified directory for duplicate files using the selected hashing mode (e.g., secure, fast, very fast).
- **delete_selected_duplicates()**: Deletes only the user-selected duplicate files.
- **delete_all_duplicates()**: Deletes all duplicate files found during the scan process.
- **open_folder_containing_file()**: Opens the folder containing the selected file from the list.
- **append_log(message)**: Appends messages to the log output area in the GUI to keep the user informed of actions.
- **run_scan()**: Runs the scan process in a separate thread to ensure that the GUI remains responsive during long scans.
- **start_scan()**: Initiates the scan process when the user clicks the "Start Scan" button.

### GUI Setup
1. **Directory Path Input**: An entry box for specifying the directory path.
2. **Hashing Technique Selector**: A dropdown menu to select the hashing technique.
3. **Log Output**: A scrolled text area to display real-time log messages and scan results.
4. **Start Scan Button**: Button to initiate the scanning process.
5. **Display Duplicates Button**: Button to display duplicates of the selected original file.
6. **Open Containing Folder Button**: Button to open the folder where the selected file is located.
7. **Delete Selected Duplicates Button**: Button to delete only the selected duplicate files.
8. **Delete All Duplicates Button**: Button to delete all found duplicate files after the scan.

### Troubleshooting

- **GUI Freezes**: The scanning process runs in a separate thread to keep the GUI responsive. If the GUI freezes, ensure that no other processes are interfering with file I/O operations, or try scanning a smaller directory.
- **Errors Reading Files**: Ensure you have appropriate file permissions and that the specified directory path is correct. Certain files may be inaccessible due to permissions, which could cause errors during scanning.

MIT License

Copyright (c) 2024 4lp1ne

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
