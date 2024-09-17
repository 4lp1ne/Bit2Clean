Byte_2_Clean

Byte_2_Clean is a Python-based tool designed to help you find and delete duplicate files from an external drive or a specific directory on your system. It calculates hashes for files, identifies duplicates, and allows you to automatically or manually remove redundant files while keeping one original. Additionally, it supports automatic progress saving and restoring if the process is interrupted.

Features
Hash-based Duplicate Detection: Scans files using MD5 hashes to detect duplicates.
Progress Save/Restore: Automatically saves progress to a progress.json file and resumes the scan if interrupted.
Manual/Automatic Deletion: Allows you to manually confirm before deleting duplicates or automatically delete them.
Progress Bar: Uses tqdm to provide real-time progress feedback.


Step-by-Step Setup Instructions
1. Clone the Repository
First, you'll need to clone the repository from GitHub:

bash

git clone https://github.com/4lp1ne/Byte_2_Clean.git
cd Byte_2_Clean
2. Set Up a Virtual Environment (Optional but Recommended)
To avoid dependency conflicts, it is recommended to set up a Python virtual environment.

For Linux/Mac:

bash

python3 -m venv env
source env/bin/activate
For Windows:

bash

python -m venv env
env\Scripts\activate
3. Install Dependencies
In the project directory, run the following command to install the required packages:

bash

pip install -r requirements.txt

This file only contains the tqdm library, as the rest of the required libraries (os, hashlib, and json) are part of Python’s standard library and do not need to be installed separately.

Running the Script

Once the dependencies are installed, you can run the script. The script will prompt you to enter the path to your external drive or directory for scanning.

bash

python byte_2_clean.py

Usage:

Scanning for Duplicates:
The script will scan the provided directory for duplicate files. It calculates the hash (using MD5) of each file and looks for duplicates.

Saving Progress:

If the process is interrupted (e.g., disk unplugged or system shutdown), the progress will be saved automatically in progress.json. The next time the script runs, it will pick up where it left off.

Manual Deletion:

Once the duplicates are found, the script will display them and ask if you want to delete them. You can decide whether to keep one file and delete the rest.

Restoring Progress:

When the process resumes, it will load progress from the progress.json file and skip over files that have already been processed.

Commands Summary

Clone the repository:

bash

git clone https://github.com/4lp1ne/Byte_2_Clean.git
cd Byte_2_Clean
Create a virtual environment (optional but recommended):

For Linux/Mac:

bash

python3 -m venv env
source env/bin/activate
For Windows:

bash

python -m venv env
env\Scripts\activate

Install dependencies:

bash

pip install -r requirements.txt

Run the script:

bash

python byte_2_clean.py


Example Project Structure
bash

Byte_2_Clean/

│

├── byte_2_clean.py      # The main Python script

├── progress.json        # Progress save file (generated at runtime)

├── README.md            # Project documentation

└── requirements.txt     # Dependency list (contains tqdm)


Possible Future Enhancements

Multi-threading support:

Add multi-threading to speed up the scanning process in large directories.

Additional hashing algorithms:

Support additional hashing algorithms like SHA-256 or SHA-1 for more security-conscious environments.

Enhanced output details:

Provide more detailed output with file sizes, timestamps, and optional file previews before deletion.

