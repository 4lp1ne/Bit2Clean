import os
import hashlib
import xxhash
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import sys

PROGRESS_FILE = 'progress.json'

# Load or initialize progress
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading {PROGRESS_FILE}: {e}. File might be corrupted.")
            return {}
    return {}


# Save progress to file
def save_progress(progress):
    try:
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress, f)
    except IOError as e:
        print(f"Error saving progress to {PROGRESS_FILE}: {e}")


# Function to hash files securely or insecurely based on user's choice
def hash_file(file_path, secure):
    if secure == '1':
        # Secure Hash (SHA-256)
        hasher = hashlib.sha256()
    else:
        # Less Secure Hash (XXHash)
        hasher = xxhash.xxh64()

    with open(file_path, 'rb') as f:
        while chunk := f.read(1024 * 1024):  # Read in chunks of 1MB
            hasher.update(chunk)

    return hasher.hexdigest()

# Function to scan a directory and find duplicate files
def scan_for_duplicates(directory, secure):
    size_map = {}
    progress = load_progress()

    # First pass: Group files by size
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in progress:
                continue  # Skip already processed files

            size = os.path.getsize(file_path)
            if size in size_map:
                size_map[size].append(file_path)
            else:
                size_map[size] = [file_path]

    # Second pass: Hash files with the same size
    hash_map = {}
    duplicates = []

    def process_file(file_path):
        if file_path in progress:
            return
        file_hash = hash_file(file_path, secure)
        if file_hash in hash_map:
            duplicates.append((file_path, hash_map[file_hash]))  # Found duplicate
        else:
            hash_map[file_hash] = file_path
        progress[file_path] = True
        save_progress(progress)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_file, file) for files in size_map.values() if len(files) > 1 for file in files]
        for _ in tqdm(futures):
            pass  # Progress bar for each thread

    return duplicates

# Delete duplicates
def delete_duplicates(duplicates, auto_delete=False):
    for duplicate, original in duplicates:
        if auto_delete:
            os.remove(duplicate)
            print(f"Deleted: {duplicate}")
        else:
            print(f"Duplicate found: {duplicate} (Original: {original})")
            delete = input("Delete this duplicate? (y/n): ")
            if delete.lower() == 'y':
                os.remove(duplicate)
                print(f"Deleted: {duplicate}")

# Main function
def main():
    directory = input("Enter the directory to scan for duplicates: ")
    secure = input("Choose hashing strategy - 1 for more secure (SHA-256), 2 for less secure (XXHash): ")

    print(f"Scanning directory '{directory}' with {'SHA-256' if secure == '1' else 'XXHash'} strategy...")

    # Scan for duplicates
    duplicates = scan_for_duplicates(directory, secure)

    # Delete duplicates (prompt or automatically based on user input)
    auto_delete = input("Automatically delete duplicates? (y/n): ").lower() == 'y'
    delete_duplicates(duplicates, auto_delete)

    print("Duplicate file scan and cleanup complete!")

if __name__ == '__main__':
    main()
