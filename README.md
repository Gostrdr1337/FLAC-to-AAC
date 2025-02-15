# 🎵 FLAC to AAC Conversion

This Python script converts audio files from FLAC format to AAC (m4a) format and creates a playlist in M3U format. The script uses the `afconvert` tool, which is available on macOS.
![Screenshot 2025-02-15 at 16 56 13](https://github.com/user-attachments/assets/4d6f3087-8de6-488e-9094-5daa616b5761)
## 📋 Requirements

- Python 3.x
- `afconvert` (available on macOS)

## 📦 Installation

1. Make sure you have Python and `afconvert` installed:
   - On macOS, `afconvert` is available by default.

2. Clone the repository:

   ```bash
   git clone https://github.com/Gostrdr1337/FLAC-to-AAC.git
   cd FLAC-to-AAC
   ```

## 🚀 Usage

1. Run the script in the terminal:

   ```bash
   python main.py
   ```

2. Follow the interactive CLI to choose the FLAC directory, AAC output directory, and start the conversion.

## 🛠️ Features

- Convert FLAC files to AAC (m4a) format.
- Generate M3U playlists.
- Interactive command-line interface.
- Save and load settings.
- Customize interface color.
- Toggle clear screen option.

## ⚙️ Settings

You can customize the following settings:

- **AAC Quality**: Set the quality of the AAC files (0-127).
- **AAC Bitrate**: Set the bitrate of the AAC files (in bits per second).
- **AAC Strategy**: Choose the encoding strategy (CBR, ABR, VBR constrained, VBR).
- **Clear Screen**: Toggle the option to clear the screen between menu displays.
- **Interface Color**: Choose the color of the interface from predefined options or enter a custom hex color code.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Enjoy converting your FLAC files to AAC! 🎧
