# Byte_2_Clean

### Overview
`Byte_2_Clean` is a Python application designed to scan directories for duplicate files using various hashing techniques. The application features a graphical user interface (GUI) built with `tkinter` and supports multiple hashing algorithms to identify and remove duplicates.
---
![Screenshot 2024-10-07 134421](https://github.com/user-attachments/assets/21fde13e-fe18-43fa-a179-158502020959)
---

### Features
- **GUI Interface**: User-friendly graphical interface for specifying directories and selecting hashing techniques.
- **Hashing Techniques**: Supports multiple hashing algorithms for scanning:
  - **SHA-256**: Secure but slower.
  - **xxhash.xxh64**: Faster but less secure.
  - **xxhash.xxh32**: Fastest but least secure.
- **Progress Tracking**: Saves and loads scan progress, allowing for efficient rescanning and preventing reprocessing of files.
- **Detailed Logging**: Real-time logging in the GUI during scanning and deletion of files.
- **Delete Functionality**: Options to delete selected or all duplicate files.

### Installation

#### Prerequisites
- **Python 3.6** or higher.

#### Install Required Packages
Run the following command to install the required Python packages:

```bash
pip install xxhash
```

### Setup

#### Clone the Repository
Clone the `Byte_2_Clean` repository to your local machine:

```bash
git clone https://github.com/4lp1ne/Byte_2_Clean.git
```

#### Navigate to the Project Directory
Change to the project directory:

```bash
cd Byte_2_Clean
```

#### Run the Application
Start the GUI application by running the Python script:

```bash
python b2c.py
```

### Requirements
Make sure the following Python packages are installed:
- **xxhash**: For fast and very fast hashing techniques.
- **tkinter**: Pre-installed with Python, used for the graphical user interface.

If you are managing dependencies using a `requirements.txt` file, create the following file:

#### `requirements.txt`
```
xxhash
```

You can install the requirements using:

```bash
pip install -r requirements.txt
```

### Using the GUI
1. **Directory Path**: Enter or select the directory you wish to scan.
2. **Select Hashing Technique**: Choose from the dropdown:
   - `"Secure"` for SHA-256 (secure but slower).
   - `"Thorough"` for xxhash.xxh64 (faster but less secure).
   - `"Quick"` for xxhash.xxh32 (fastest but least secure).
3. **Start Scan**: Click the "Start Scan" button to begin the scan.
4. **View Duplicates**: After scanning, select an original file and click "Display Duplicates of Selected Original" to view duplicates.
5. **Delete Duplicates**:
   - Use "Delete Selected Duplicates" to remove selected duplicates.
   - Use "Delete All Duplicates" to remove all duplicates found in the scan.
6. **Open Folder**: Select a file and click "Open Containing Folder" to open the folder containing the selected file.
7. **Log Output**: View real-time logs showing progress and detailed information.

### Code Description

#### Main Functions
- **save_progress(progress)**: Saves the scan progress to a JSON file for resuming later.
- **load_progress()**: Loads saved scan progress to prevent reprocessing already scanned files.
- **compute_hash(file_path, hash_func_cls)**: Computes the hash of a file using the selected hashing algorithm.
- **scan_for_duplicates(directory, mode)**: Scans the specified directory for duplicate files based on the selected hashing mode.
- **delete_selected_duplicates()**: Deletes only the selected duplicate files.
- **delete_all_duplicates()**: Deletes all duplicates found during the scan.
- **open_folder_containing_file()**: Opens the folder where a selected file resides.
- **append_log(message)**: Adds messages to the GUI’s log output to display the scanning and deletion processes.
- **run_scan()**: Runs the scanning process in a separate thread, ensuring the GUI remains responsive during long scans.
- **start_scan()**: Starts the scan when the "Start Scan" button is pressed.

#### GUI Elements
- **Directory Path Input**: Input box for specifying the directory to be scanned.
- **Hashing Technique Dropdown**: Dropdown to select the hashing method (SHA-256, xxhash.xxh64, xxhash.xxh32).
- **Log Output**: A scrollable text box that displays real-time logs during scanning and deletion.
- **Buttons**:
  - **Start Scan**: Initiates the scanning process.
  - **Display Duplicates of Selected Original**: Displays duplicates of the selected original file.
  - **Open Containing Folder**: Opens the folder of the selected file.
  - **Delete Selected Duplicates**: Deletes the duplicates selected by the user.
  - **Delete All Duplicates**: Deletes all detected duplicate files.
  - **Reset Progress**: Resets the scan progress by deleting the saved progress file.

### Troubleshooting

- **GUI Freezes**: Ensure the scan process runs in a separate thread. If the GUI becomes unresponsive, verify that no other processes are blocking file I/O.
- **Errors Reading Files**: Check file permissions and verify that the directory path is correct.

### License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

### MIT License

```text
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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

