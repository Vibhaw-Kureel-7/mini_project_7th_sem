import os
import zipfile

# Map of original folder -> base new name (without index prefix)
RENAMING_MAP = {
    "lora_adapters_ch1": "CrisisCore",
    "lora_adapters_ch2": "AtmaAnalytics",
    "lora_adapters_ch3": "ActionFlow",
    "lora_adapters_ch4": "Karmicknowledge",
    "lora_adapters_ch5": "ZenithOS",
    "lora_adapters_ch6": "Mindful Modulator",
    "lora_adapters_ch7": "SourceCode",
    "lora_adapters_ch8": "Continuum",
    "lora_adapters_ch9": "OmniPresence",
    "lora_adapters_ch10": "AweMatrix",
    "lora_adapters_ch11": "CosmosView",
    "lora_adapters_ch12": "DevotionAl",
    "lora_adapters_ch13": "FieldScanner",
    "lora_adapters_ch14": "GunaClassifier",
    "lora_adapters_ch15": "NexusCut",
    "lora_adapters_ch16": "VirtueCompass",
    "lora_adapters_ch17": "LifestyleOps",
    "lora_adapters_ch18": "MokshaPath",
}

def process_lora_adapters():
    """
    Runs a 3-phase process in the current directory:
    1. Unzips all 'lora_adapters_ch*.zip' files.
    2. Renames the extracted folders based on RENAMING_MAP, adding numeric prefixes (1_, 2_, etc.).
    3. Zips all renamed folders into a single 'lora_adapters.zip'.
    """
    current_directory = os.getcwd()
    print(f"--- 📂 Scanning folder: {current_directory} ---")

    # --- 1. Unzip Phase ---
    print("\n--- 1. Unzipping Files ---")
    found_zips = 0
    for original_folder in RENAMING_MAP.keys():
        zip_filename = f"{original_folder}.zip"
        full_zip_path = os.path.join(current_directory, zip_filename)

        if os.path.exists(full_zip_path):
            print(f"Extracting '{zip_filename}'...")
            try:
                with zipfile.ZipFile(full_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(current_directory)
                print(f"  -> Done.")
                found_zips += 1
            except zipfile.BadZipFile:
                print(f"  -> ERROR: '{zip_filename}' is corrupted.")
            except Exception as e:
                print(f"  -> ERROR: {e}")
        else:
            print(f"Warning: Zip file '{zip_filename}' not found. Skipping.")

    if found_zips == 0:
        print("\nNo zip files were found to extract. Exiting.")
        return

    # --- 2. Rename Phase ---
    print("\n--- 2. Renaming Folders ---")
    renamed_count = 0
    indexed_map = {}
    for idx, (original_folder, base_name) in enumerate(RENAMING_MAP.items(), start=1):
        new_name = f"{idx}_{base_name.replace(' ', '_')}"  # Add numeric prefix + replace spaces
        original_path = os.path.join(current_directory, original_folder)
        new_path = os.path.join(current_directory, new_name)
        indexed_map[original_folder] = new_name

        if os.path.isdir(original_path):
            if os.path.isdir(new_path):
                print(f"Warning: Target '{new_name}' already exists. Skipping rename.")
            else:
                try:
                    os.rename(original_path, new_path)
                    print(f"Renamed '{original_folder}'  ->  '{new_name}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"ERROR: Could not rename '{original_folder}': {e}")
        else:
            print(f"Info: '{original_folder}' not found. (Already renamed?)")

    # --- 3. Zip All Renamed Folders into One ---
    print("\n--- 3. Creating single 'lora_adapters.zip' ---")

    folders_to_zip = list(indexed_map.values())
    output_zip_filename = "lora_adapters.zip"

    try:
        with zipfile.ZipFile(output_zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            total_files_added = 0
            folders_added_count = 0

            for folder_name in folders_to_zip:
                folder_path = os.path.join(current_directory, folder_name)

                if not os.path.isdir(folder_path):
                    print(f"Warning: Folder '{folder_name}' not found. Skipping.")
                    continue

                print(f"Adding folder '{folder_name}' to zip...")
                folders_added_count += 1

                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, current_directory)
                        zf.write(file_path, archive_name)
                        total_files_added += 1

        print(f"\nSuccessfully created '{output_zip_filename}'.")
        print(f"Added {folders_added_count} folders ({total_files_added} total files) to the archive.")

    except Exception as e:
        print(f"\nERROR: Failed to create '{output_zip_filename}': {e}")

    print("\n--- ✅ All tasks complete ---")
    print(f"Unzipped {found_zips} files.")
    print(f"Renamed {renamed_count} folders.")
    print(f"Created new archive '{output_zip_filename}'.")


if __name__ == "__main__":
    process_lora_adapters()
