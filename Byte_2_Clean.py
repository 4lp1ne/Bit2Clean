import os
import hashlib
import xxhash
import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from concurrent.futures import ThreadPoolExecutor


# Save progress to a JSON file
def save_progress(progress):
    try:
        with open('progress.json', 'w') as f:
            json.dump(progress, f)
        append_log("Progress saved successfully.")
    except Exception as e:
        append_log(f"Failed to save progress: {e}")


# Load progress from the JSON file
def load_progress():
    progress_file = 'progress.json'
    append_log(f"Loading progress from {progress_file}...")

    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                progress = json.load(f)
            append_log("Progress loaded successfully.")
            return progress
        except json.JSONDecodeError as e:
            append_log(f"Error decoding JSON from {progress_file}: {e}")
            append_log("Backing up corrupted progress file and starting fresh.")
            os.rename(progress_file, f"{progress_file}.backup")
            return {'processed_files': [], 'duplicates': []}
    else:
        append_log("No progress file found. Starting fresh.")
        return {'processed_files': [], 'duplicates': []}


# Function to compute file hash using specified algorithm
def compute_hash(file_path, hash_func_cls):
    try:
        append_log(f"Computing hash for {file_path}...")
        hash_func = hash_func_cls()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Read in larger chunks
                hash_func.update(chunk)
        hash_value = hash_func.hexdigest()
        append_log(f"Hash computed for {file_path}: {hash_value}")
        return hash_value
    except (OSError, IOError) as e:
        append_log(f"Error reading file {file_path}: {e}")
        return None


# Scan directory for duplicates in various modes
def scan_for_duplicates(directory, mode='secure'):
    processed_files = {}
    duplicate_files = []

    append_log(f"Starting scan in '{mode}' mode...")
    progress = load_progress()
    processed_files = {item['path']: item['hash'] for item in progress['processed_files']}
    duplicate_files = progress['duplicates']

    if mode == 'very_fast':
        hash_func_cls = xxhash.xxh32
        append_log("Using xxhash.xxh32 for very fast mode.")
    elif mode == 'fast':
        hash_func_cls = xxhash.xxh64
        append_log("Using xxhash.xxh64 for fast mode.")
    else:
        hash_func_cls = hashlib.sha256
        append_log("Using SHA-256 for secure mode.")

    try:
        # Collect all file paths
        file_paths = []
        append_log("Collecting file paths...")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

        append_log(f"Total files to process: {len(file_paths)}")

        # Process files in parallel to compute hashes
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(compute_hash, file_path, hash_func_cls) for file_path in file_paths]

            for file_path, future in zip(file_paths, futures):
                file_hash = future.result()
                if file_hash is None:
                    append_log(f"Skipping file {file_path} due to read error.")
                    continue

                if file_hash in processed_files.values():
                    duplicate_files.append(file_path)
                    append_log(f"Duplicate found: {file_path}")
                else:
                    processed_files[file_path] = file_hash
                    append_log(f"File processed: {file_path}")

        # Save progress at the end of the scan
        append_log("Scan complete. Saving final progress...")
        save_progress({
            'processed_files': [{'path': path, 'hash': hash} for path, hash in processed_files.items()],
            'duplicates': duplicate_files
        })

    except KeyboardInterrupt:
        append_log("\nScan interrupted. Saving progress...")
        save_progress({
            'processed_files': [{'path': path, 'hash': hash} for path, hash in processed_files.items()],
            'duplicates': duplicate_files
        })
        append_log("Progress saved. Exiting gracefully.")

    return duplicate_files


# Ask user for confirmation to delete all duplicates
def delete_duplicates():
    duplicates = scan_for_duplicates(path_entry.get(), hash_option.get())
    if not duplicates:
        append_log("No duplicates found.")
        return

    append_log(f"\n{len(duplicates)} duplicate files found.")
    for file_path in duplicates:
        try:
            os.remove(file_path)
            append_log(f"Deleted {file_path}.")
        except OSError as e:
            append_log(f"Error deleting file {file_path}: {e}")


# Append log to the text widget in the GUI
def append_log(message):
    log_area.insert(tk.END, message + '\n')
    log_area.yview(tk.END)


# Function to run the scan in a separate thread
def run_scan():
    # Disable the button and update GUI to show the scan is in progress
    start_button.config(state=tk.DISABLED)
    directory = path_entry.get()
    mode = hash_option.get()

    append_log(f"Scanning directory '{directory}' with {mode} mode...")

    # Start the scan
    scan_for_duplicates(directory, mode)

    # Re-enable the button after scan completion
    start_button.config(state=tk.NORMAL)


# Start scanning process
def start_scan():
    # Run the scan in a separate thread to keep the GUI responsive
    threading.Thread(target=run_scan, daemon=True).start()


# GUI setup
root = tk.Tk()
root.title("4lp1ne > Duplicate File Scanner < ɘn1ql4")

# Directory Path
tk.Label(root, text="Directory Path:").pack(pady=5)
path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=5)

# Hash Technique
tk.Label(root, text="Select Hashing Technique:").pack(pady=5)
hash_option = ttk.Combobox(root, values=["secure", "fast", "very_fast"], state="readonly")
hash_option.set("secure")  # Default selection
hash_option.pack(pady=5)

# Log Output
tk.Label(root, text="Log Output:").pack(pady=5)
log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=80)
log_area.pack(pady=5)

# Start Button
start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.pack(pady=5)

# Delete Duplicates Button
delete_button = tk.Button(root, text="Delete Duplicates", command=delete_duplicates)
delete_button.pack(pady=10)

root.mainloop()
