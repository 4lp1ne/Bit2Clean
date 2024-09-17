Byte_2_Clean


is a Python-based tool designed to help you find and delete duplicate files from an external drive or a specific directory on your system. It calculates hashes for files, identifies duplicates, and allows you to automatically or manually remove redundant files while keeping one original. Additionally, it supports automatic progress saving and restoring if the process is interrupted.

Features:
Hash-based Duplicate Detection: Scans files using MD5 hashes to detect duplicates.
Progress Save/Restore: Automatically saves progress to a progress.json file and resumes the scan if interrupted.
Manual/Automatic Deletion: Allows you to manually confirm before deleting duplicates or automatically delete them.
Progress Bar: Uses tqdm to provide real-time progress feedback.
Step-by-Step Setup Instructions:
1. Clone the Repository
First, you'll need to clone the repository from GitHub.

bash
Copy code
git clone https://github.com/4lp1ne/Byte_2_Clean.git
cd Byte_2_Clean
2. Set Up a Virtual Environment (Optional but Recommended)
To avoid dependency conflicts, it’s a good idea to set up a virtual environment.

For Linux/Mac:

bash
Copy code
python3 -m venv env
source env/bin/activate
For Windows:

bash
Copy code
python -m venv env
env\Scripts\activate
3. Install Dependencies
In the project directory, run the following command to install the required packages.

bash
Copy code
pip install -r requirements.txt
requirements.txt:
Here’s the content of the requirements.txt:

Copy code
tqdm
This file only contains tqdm, as the rest of the libraries (such as os, hashlib, and json) are part of Python’s standard library and do not need to be installed.

4. Running the Script
Once the dependencies are installed, you can run the script. The script will prompt you to enter the path to your external drive or directory for scanning.

bash
Copy code
python byte_2_clean.py
Usage:
Scanning for Duplicates: The script will first scan the provided directory for duplicate files. It will calculate the hash of each file and look for duplicates.

Saving Progress: If the process is interrupted (e.g., disk unplugged or a system reboot), the progress will be saved automatically in progress.json. The next time the script runs, it will pick up where it left off.

Manual Deletion: Once the duplicates are found, the script will display them and ask if you want to delete them. You can decide whether to keep one file and delete the rest.

Restoring Progress: When the process resumes, it will load the progress from the progress.json file and skip over any files that were already processed.

Commands Summary:
Clone the repository:

bash
Copy code
git clone https://github.com/4lp1ne/Byte_2_Clean.git
cd Byte_2_Clean
Create a virtual environment (optional but recommended):

Linux/Mac:

bash
Copy code
python3 -m venv env
source env/bin/activate
Windows:

bash
Copy code
python -m venv env
env\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the script:

bash
Copy code
python byte_2_clean.py
Example Project Structure:
bash
Copy code
Byte_2_Clean/
│
├── byte_2_clean.py      # The main Python script with the code provided
├── progress.json        # The file where progress is saved (generated at runtime)
├── README.md            # Project documentation (this could be what you're writing)
└── requirements.txt     # Dependency list for installing tqdm
Possible Future Enhancements:
Add multi-threading support to speed up scanning large directories.
Support additional hashing algorithms (like SHA-256).
Provide a more detailed output with file sizes, timestamps, or even file previews.
