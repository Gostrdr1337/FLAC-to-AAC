import subprocess
import os
import shutil

def convert_flac_to_aac(flac_file_path, aac_file_path, cover_file_path, file_number, quality, bitrate, strategy, cover_exists):
    try:
        print(f"\n\033[94mConverting file number {file_number}: {os.path.basename(flac_file_path)}")
        command = f'afconvert "{flac_file_path}" -o "{aac_file_path}" -f m4af -d aac -q {quality} -b {bitrate} -s {strategy} -c 2'
        subprocess.call(command, shell=True)
        if cover_exists:
            shutil.copy(cover_file_path, os.path.dirname(aac_file_path))
        print(f"\033[92mConversion completed for file number {file_number}: {os.path.basename(flac_file_path)}\n")
    except Exception as e:
        print(f"\033[91mError converting file {flac_file_path}: {e}")

def get_name_and_date(folder_name):
    try:
        name_and_date = folder_name.split("[")[0].strip()
        name_and_date += " [AAC] [256kbps]"
        return name_and_date
    except Exception as e:
        print(f"\033[91mError getting name and date from folder name {folder_name}: {e}")
        return folder_name

def convert_directory(input_directory, output_directory, quality, bitrate, strategy):
    if not os.path.isdir(input_directory) or not os.path.isdir(output_directory):
        print(f"\033[91mInvalid directory paths provided.")
        return

    for foldername, _, filenames in os.walk(input_directory):
        flac_files = [f for f in filenames if f.endswith(".flac") and not f.startswith('._')]
        if flac_files:
            try:
                name_and_date = get_name_and_date(os.path.basename(foldername))
                aac_folder_name = f"{name_and_date}"
                aac_folder_path = os.path.join(output_directory, aac_folder_name)
                if not os.path.exists(aac_folder_path):
                    os.makedirs(aac_folder_path)

                aac_files = []
                cover_file_path = None
                for ext in ['jpg', 'jpeg', 'png']:
                    potential_cover = os.path.join(foldername, f"cover.{ext}")
                    if os.path.exists(potential_cover):
                        cover_file_path = potential_cover
                        break
                cover_exists = cover_file_path is not None
                if not cover_exists:
                    print(f"\n\033[93mWarning: No cover file found in {foldername}. Skipping cover copy for all files.\n")

                for file_number, filename in enumerate(sorted(flac_files), 1):
                    flac_file_path = os.path.join(foldername, filename)
                    aac_file_path = os.path.join(aac_folder_path, filename.replace(".flac", ".m4a"))
                    convert_flac_to_aac(flac_file_path, aac_file_path, cover_file_path, file_number, quality, bitrate, strategy, cover_exists)
                    aac_files.append(os.path.basename(aac_file_path))

                if aac_files:
                    m3u_filename = f"{name_and_date}.m3u"
                    m3u_path = os.path.join(aac_folder_path, m3u_filename)
                    with open(m3u_path, 'w') as m3u_file:
                        for i, aac_file in enumerate(aac_files, 1):
                            m3u_file.write(f"{i}. {aac_file}\n")
            except Exception as e:
                print(f"\033[91mError processing folder {foldername}: {e}")
