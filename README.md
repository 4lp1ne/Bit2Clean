Byte_2_Clean
Overview
Byte_2_Clean is a Python application designed to scan directories for duplicate files using various hashing techniques. The application features a graphical user interface (GUI) built with tkinter and supports multiple hashing algorithms to identify duplicates.

Features
GUI Interface: User-friendly graphical interface for specifying the directory and choosing the hashing technique.
Hashing Techniques: Supports SHA-256 (secure), xxhash.xxh64 (fast), and xxhash.xxh32 (very fast).
Progress Tracking: Saves and loads scan progress for efficient processing.
Detailed Logging: Displays logs and scan results in the GUI.
Installation
Prerequisites
Python 3.6 or higher
Install Required Packages
To install the required Python packages, run the following command:

sh
Copy code
pip install xxhash
Setup
Clone the Repository

Clone the repository to your local machine:

sh
Copy code
git clone https://github.com/4lp1ne/Byte_2_Clean.git
Navigate to the Project Directory

Change to the project directory:

sh
Copy code
cd Byte_2_Clean
Usage
Run the Application

Execute the Python script to start the GUI application:

sh
Copy code
python duplicate_file_scanner.py
Using the GUI

Directory Path: Enter the directory path you want to scan in the input field.
Select Hashing Technique: Choose from the dropdown menu:
"secure" for SHA-256 (more secure but slower)
"fast" for xxhash.xxh64 (faster but less secure)
"very_fast" for xxhash.xxh32 (fastest but least secure)
Start Scan: Click the "Start Scan" button to begin scanning.
Delete Duplicates: After scanning, click the "Delete Duplicates" button to remove all detected duplicates.
The log output area will show detailed information about the scanning and deletion processes.

Code Description
Main Functions
save_progress(progress): Saves the current scan progress to a JSON file.
load_progress(): Loads scan progress from the JSON file.
compute_hash(file_path, hash_func_cls): Computes the hash of a file using the specified hashing function.
scan_for_duplicates(directory, mode='secure'): Scans the specified directory for duplicate files using the selected hashing mode.
delete_duplicates(): Deletes all duplicate files found during the scan.
append_log(message): Appends messages to the log output area in the GUI.
run_scan(): Runs the scan process in a separate thread to keep the GUI responsive.
start_scan(): Starts the scan process in a new thread.
GUI Setup
Directory Path Input: Entry box for specifying the directory path.
Hashing Technique Selector: Dropdown menu to select the hashing technique.
Log Output: Scrolled text area to display log messages.
Start Scan Button: Button to initiate the scanning process.
Delete Duplicates Button: Button to delete all found duplicate files.
Troubleshooting
GUI Freezes: The scanning process runs in a separate thread to keep the GUI responsive. If the GUI freezes, ensure that no other processes are running that may interfere with file I/O operations.
Errors Reading Files: Check file permissions and ensure the specified directory path is correct.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Contributions are welcome! Please submit issues or pull requests to improve the application.

Contact
For questions or support, please open an issue in the GitHub repository.

