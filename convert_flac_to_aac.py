import subprocess
import os
import shutil

# Function to convert FLAC to AAC
def convert_flac_to_aac(flac_file_path, aac_file_path, cover_file_path, file_number):
    command = f'afconvert "{flac_file_path}" -o "{aac_file_path}" -f m4af -d aac -q 127 -b 256000 -s 0 -c 2'
    subprocess.call(command, shell=True)
    shutil.copy(cover_file_path, os.path.dirname(aac_file_path))  # Copy cover.jpg to the output directory
    print(f"\033[92mConversion completed for file number {file_number}: {os.path.basename(flac_file_path)}")

# Function to get the name and date from the folder name
def get_name_and_date(folder_name):
    name_and_date = folder_name.split("[")[0].strip()  # Remove everything after the first occurrence of "["
    name_and_date += " [AAC] [256kbps]"
    return name_and_date

# Function to convert all FLAC files in a directory
def convert_directory(input_directory, output_directory):
    if not os.path.isdir(input_directory) or not os.path.isdir(output_directory):
        return

    for foldername, _, filenames in os.walk(input_directory):
        if filenames:
            name_and_date = get_name_and_date(os.path.basename(foldername))
            aac_folder_name = f"{name_and_date}"
            aac_folder_path = os.path.join(output_directory, aac_folder_name)
            if not os.path.exists(aac_folder_path):
                os.makedirs(aac_folder_path)

            aac_files = []  # List to store names of AAC files

            for filename in sorted(filenames):  # Sort filenames
                if filename.startswith('._'):
                    continue
                flac_file_path = os.path.join(foldername, filename)
                if flac_file_path.endswith(".flac"):
                    aac_file_path = os.path.join(aac_folder_path, filename.replace(".flac", ".m4a"))
                    cover_file_path = os.path.join(foldername, "cover.jpg")
                    convert_flac_to_aac(flac_file_path, aac_file_path, cover_file_path, 1)
                    aac_files.append(os.path.basename(aac_file_path))

            # Generate m3u playlist
            m3u_filename = f"{name_and_date}.m3u"
            m3u_path = os.path.join(aac_folder_path, m3u_filename)
            with open(m3u_path, 'w') as m3u_file:
                for i, aac_file in enumerate(aac_files, 1):
                    m3u_file.write(f"{i}. {aac_file}\n")  # Write AAC file names with numbers to the m3u playlist

# Function for interactive command-line interface
def interactive_cli():
    input_directory = None
    output_directory = None

    print("\033[95m")
    print(r"""
     _____ _        _    ____      _                _        _    ____
    |  ___| |      / \  / ___|    | |_ ___         / \      / \  / ___|
    | |_  | |     / _ \| |   _____| __/ _ \ _____ / _ \    / _ \| |
    |  _| | |___ / ___ \ |__|_____| || (_) |_____/ ___ \  / ___ \ |___
    |_|   |_____/_/   \_\____|     \__\___/     /_/   \_\/_/   \_\____|
                                                                       """)
    print("-" * 70)

    while True:
        print("\033[96m")
        print("\n1. Choose FLAC directory")
        print("2. Choose AAC output directory")
        print("3. Start conversion")
        print("4. Exit")
        option = input("\nSelect an option: ")

        if option == "1":
            input_directory = input("\nEnter the path to the FLAC directory: ")
            if not os.path.isdir(input_directory):
                print(f"The directory {input_directory} does not exist.")
                input_directory = None
        elif option == "2":
            output_directory = input("\nEnter the path to the AAC output directory: ")
            if not os.path.isdir(output_directory):
                print(f"The directory {output_directory} does not exist.")
                output_directory = None
        elif option == "3":
            if input_directory is not None and output_directory is not None:
                print("\033[94mStarting conversion...")
                convert_directory(input_directory, output_directory)
                print("\033[92mConversion completed.")
            else:
                print("\033[91mYou must first choose the FLAC and AAC directories.")
        elif option == "4":
            break
        else:
            print("\033[91mUnknown option. Please select a valid option.")

interactive_cli()

