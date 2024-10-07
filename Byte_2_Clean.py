import os
import hashlib
import xxhash
import json
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from concurrent.futures import ThreadPoolExecutor
import subprocess  # To open files with the default system application

# Append log to the text widget in the GUI
def append_log(message):
    log_area.insert(tk.END, message + '\n')
    log_area.yview(tk.END)

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

# Function to update progress bar and status label
def update_progress(current, total):
    progress = (current / total) * 100
    progress_var.set(progress)
    status_label.config(text=f"Scanning... {int(progress)}% complete")

# Function to display unique files based on button click (either original or duplicate)
def display_files(files, title="Files"):
    unique_files = list(set(files))  # Ensure no duplicates are shown
    file_listbox.delete(0, tk.END)  # Clear the listbox
    for file in unique_files:
        file_listbox.insert(tk.END, file)  # Insert new unique files
    listbox_label.config(text=title)

# Function to open the folder containing the selected file
def open_folder_containing_file(listbox):
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No file selected", "Please select a file to open its folder.")
        return
    file_path = listbox.get(selected_index[0])
    directory_path = os.path.dirname(file_path)
    try:
        if os.name == 'nt':  # Windows
            os.startfile(directory_path)
        elif os.name == 'posix':  # MacOS or Linux
            subprocess.call(['xdg-open', directory_path])
    except Exception as e:
        append_log(f"Failed to open folder: {e}")

# Scan directory for duplicates in various modes
def scan_for_duplicates(directory, mode='Quick Scan'):
    processed_files = {}
    duplicate_files = {}
    file_hash_map = {}  # Mapping of file hash -> list of file paths

    append_log(f"Starting scan in '{mode}' mode...")

    progress = load_progress()
    processed_files = {item['path']: item['hash'] for item in progress['processed_files']}

    if mode == 'Quick Scan':
        hash_func_cls = xxhash.xxh32
        append_log("Using xxhash.xxh32 for quick scan mode.")
    elif mode == 'Thorough Scan':
        hash_func_cls = xxhash.xxh64
        append_log("Using xxhash.xxh64 for thorough scan.")
    else:
        hash_func_cls = hashlib.sha256
        append_log("Using SHA-256 for secure scan.")

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

            for i, (file_path, future) in enumerate(zip(file_paths, futures)):
                file_hash = future.result()
                if file_hash is None:
                    append_log(f"Skipping file {file_path} due to read error.")
                    continue

                # Store the file path by hash in file_hash_map
                file_hash_map.setdefault(file_hash, []).append(file_path)

                update_progress(i + 1, len(file_paths))

        # Save progress at the end of the scan
        append_log("Scan complete. Saving final progress...")
        save_progress({
            'processed_files': [{'path': path, 'hash': hash} for path, hash in processed_files.items()],
            'duplicates': [{'hash': hash, 'path': p} for hash, paths in file_hash_map.items() if len(paths) > 1 for p in paths[1:]]
        })

    except KeyboardInterrupt:
        # Handle interruptions gracefully
        append_log("\nScan interrupted. Saving progress...")
        save_progress({
            'processed_files': [{'path': path, 'hash': hash} for path, hash in processed_files.items()],
            'duplicates': [{'hash': hash, 'path': p} for hash, paths in file_hash_map.items() if len(paths) > 1 for p in paths[1:]]
        })

    return file_hash_map

# Function to calculate total file size
def calculate_total_size(files):
    total_size = sum(os.path.getsize(file) for file in files)
    return total_size / (1024 * 1024)  # Convert to MB

# Reset the progress file
def reset_progress():
    progress_file = 'progress.json'
    if os.path.exists(progress_file):
        try:
            os.remove(progress_file)
            append_log("Progress reset successfully. You can start fresh.")
        except Exception as e:
            append_log(f"Failed to reset progress: {e}")
    else:
        append_log("No progress file found to reset.")

# Function to select a directory
def choose_directory():
    directory = filedialog.askdirectory()
    if directory:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory)

# Function to delete selected duplicates
def delete_selected_duplicates():
    selected_indices = file_listbox.curselection()
    selected_files = [file_listbox.get(i) for i in selected_indices]

    if not selected_files:
        append_log("No duplicates selected for deletion.")
        return

    append_log(f"\nDeleting {len(selected_files)} selected duplicate files...")
    for file_path in selected_files:
        try:
            os.remove(file_path)
            append_log(f"Deleted {file_path}.")
        except OSError as e:
            append_log(f"Error deleting file {file_path}: {e}")

# Function to delete all duplicates
def delete_all_duplicates():
    all_duplicates = [p for file_paths in file_hash_map.values() if len(file_paths) > 1 for p in file_paths[1:]]
    if all_duplicates:
        append_log(f"\nDeleting {len(all_duplicates)} duplicate files...")
        for file_path in all_duplicates:
            try:
                os.remove(file_path)
                append_log(f"Deleted {file_path}.")
            except OSError as e:
                append_log(f"Error deleting file {file_path}: {e}")
    else:
        append_log("No duplicates available for deletion.")

# Function to display duplicates of the selected original
def display_duplicates_for_selected_original():
    selected_index = file_listbox.curselection()
    if not selected_index:
        messagebox.showwarning("No file selected", "Please select an original file.")
        return

    selected_file = file_listbox.get(selected_index[0])

    # Find the corresponding hash for the selected file
    for file_hash, file_paths in file_hash_map.items():
        if file_paths[0] == selected_file:
            # Show all duplicates (excluding the original)
            duplicates = file_paths[1:]
            display_files(duplicates, title="Duplicate Files")
            break

# Function to run the scan in a separate thread
def run_scan():
    # Clear the log area and listbox before starting a new scan
    log_area.delete(1.0, tk.END)  # Clear the log area
    file_listbox.delete(0, tk.END)  # Clear the file listbox
    
    start_button.config(state=tk.DISABLED)
    directory = path_entry.get()
    mode = hash_option.get()

    append_log(f"Scanning directory '{directory}' with {mode} mode...")

    # Start the scan
    global file_hash_map
    file_hash_map = scan_for_duplicates(directory, mode)

    start_button.config(state=tk.NORMAL)
    
    if file_hash_map:
        # Show only the original files (first occurrence of each file)
        original_files = [file_paths[0] for file_paths in file_hash_map.values() if len(file_paths) > 1]
        total_size = calculate_total_size(original_files)
        append_log(f"Total original files: {len(original_files)}, Total size: {total_size:.2f} MB")
        display_files(original_files, title="Original Files")
        messagebox.showinfo("Scan Complete", f"Found {len(original_files)} original files totaling {total_size:.2f} MB.")
    else:
        append_log("No duplicates found.")
        messagebox.showinfo("Scan Complete", "No duplicate files found.")

# ** Start scanning process - this must be defined before we use it! **
def start_scan():
    threading.Thread(target=run_scan, daemon=True).start()

# Main GUI setup
root = tk.Tk()
root.title("4lp1ne > Duplicate File Scanner < ɘn1ql4")
root.geometry("420x490")  # Scale down the size to 70%

# Directory Path and Choose Button
tk.Label(root, text="Directory Path:").pack(pady=5)
path_frame = tk.Frame(root)
path_frame.pack(pady=5)
path_entry = tk.Entry(path_frame, width=40)
path_entry.pack(side=tk.LEFT, padx=5)
choose_button = tk.Button(path_frame, text="Choose Folder", command=choose_directory)
choose_button.pack(side=tk.LEFT)

# Scan Type (Simplified)
tk.Label(root, text="Select Scan Type:").pack(pady=5)
hash_option = ttk.Combobox(root, values=["Quick Scan", "Thorough Scan", "Secure Scan"], state="readonly")
hash_option.set("Quick Scan")
hash_option.pack(pady=5)

# Log Output
tk.Label(root, text="Log Output:").pack(pady=5)
log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=8, width=60)
log_area.pack(pady=5)

# Progress Bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=5)

# Status Label
status_label = tk.Label(root, text="Idle", anchor='w')
status_label.pack(pady=5, fill='x')

# Listbox to display files (either original or duplicate)
tk.Label(root, text="Files:").pack(pady=5)
file_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=60, height=6)
file_listbox.pack(pady=5)

# Label to update based on whether we display original or duplicate files
listbox_label = tk.Label(root, text="Files")
listbox_label.pack(pady=5)

# Frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Buttons to display original or duplicate files
original_button = tk.Button(button_frame, text="Display Duplicates of Selected Original", command=display_duplicates_for_selected_original)
original_button.grid(row=0, column=0, padx=5, pady=5)

# Open Folder Button
open_button = tk.Button(button_frame, text="Open Containing Folder", command=lambda: open_folder_containing_file(file_listbox))
open_button.grid(row=0, column=1, padx=5, pady=5)

# Delete Selected Button
delete_selected_button = tk.Button(button_frame, text="Delete Selected Duplicates", command=delete_selected_duplicates)
delete_selected_button.grid(row=1, column=0, padx=5, pady=5)

# Delete All Button
delete_all_button = tk.Button(button_frame, text="Delete All Duplicates", command=delete_all_duplicates)
delete_all_button.grid(row=1, column=1, padx=5, pady=5)

# Start Button
start_button = tk.Button(root, text="Start Scan", command=start_scan)
start_button.pack(pady=5)

# Reset Button
reset_button = tk.Button(root, text="Reset Progress", command=reset_progress)
reset_button.pack(pady=5)

root.mainloop()
