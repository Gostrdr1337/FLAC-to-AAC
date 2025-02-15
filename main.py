import os
import shlex
from src.settings import load_settings, save_settings
from src.conversion import convert_directory
from src.utils import clear_terminal, color_to_readable

def interactive_cli():
    settings = load_settings()
    quality = settings.get("quality", 127)
    bitrate = settings.get("bitrate", 256000)
    strategy = settings.get("strategy", 0)
    clear_screen = settings.get("clear_screen", True)
    interface_color = settings.get("interface_color", "\033[96m")

    input_directory = None
    output_directory = None

    try:
        while True:
            if clear_screen:
                clear_terminal()
            print(interface_color)
            print(r"""
             _____ _        _    ____      _                _        _    ____
            |  ___| |      / \  / ___|    | |_ ___         / \      / \  / ___|
            | |_  | |     / _ \| |   _____| __/ _ \ _____ / _ \    / _ \| |
            |  _| | |___ / ___ \ |__|_____| || (_) |_____/ ___ \  / ___ \ |___
            |_|   |_____/_/   \_\____|     \__\___/     /_/   \_\/_/   \_\____|
                                                                               """)
            print("-" * 70)

            print(interface_color)
            print("\n1. Choose FLAC directory")
            print("2. Choose AAC output directory")
            print("3. Start conversion")
            print("4. Settings")
            print("5. Show current settings")
            print("6. Exit")
            option = input("\nSelect an option: ")

            if option == "1":
                input_directory = input("\nEnter the path to the FLAC directory: ")
                input_directory = os.path.normpath(shlex.split(input_directory)[0])
                if not os.path.isdir(input_directory):
                    print(f"\033[91mThe directory {input_directory} does not exist.")
                    input_directory = None
                else:
                    print(f"\033[92mFLAC directory set to: {input_directory}")
            elif option == "2":
                output_directory = input("\nEnter the path to the AAC output directory: ")
                output_directory = os.path.normpath(shlex.split(output_directory)[0])
                if not os.path.isdir(output_directory):
                    print(f"\033[91mThe directory {output_directory} does not exist.")
                    output_directory = None
                else:
                    print(f"\033[92mAAC output directory set to: {output_directory}")
            elif option == "3":
                if input_directory is not None and output_directory is not None:
                    if clear_screen:
                        clear_terminal()
                    print("\n\033[94mStarting conversion...\n")
                    try:
                        convert_directory(input_directory, output_directory, quality, bitrate, strategy)
                        print("\033[92mConversion completed.")
                    except Exception as e:
                        print(f"\033[91mError during conversion: {e}")
                    input("\nPress Enter to return to the main menu...")
                else:
                    print("\033[91mYou must first choose the FLAC and AAC directories.")
            elif option == "4":
                while True:
                    if clear_screen:
                        clear_terminal()
                    print(interface_color)
                    print("\nSettings")
                    print("1. Interface Settings")
                    print("2. Quality Settings")
                    print("3. Save settings")
                    print("4. Back to main menu")
                    sub_option = input("\nSelect an option: ")

                    if sub_option == "1":
                        while True:
                            if clear_screen:
                                clear_terminal()
                            print(interface_color)
                            print("\nInterface Settings")
                            print("1. Toggle clear screen (current: {})".format("On" if clear_screen else "Off"))
                            print("2. Change interface color")
                            print("3. Back to settings menu")
                            interface_option = input("\nSelect an option: ")

                            if interface_option == "1":
                                clear_screen = not clear_screen
                                print(f"\033[92mClear screen set to: {'On' if clear_screen else 'Off'}")
                            elif interface_option == "2":
                                print("\033[93m")
                                print("Choose interface color:")
                                print("1: Blue")
                                print("2: Green")
                                print("3: Yellow")
                                print("4: Red")
                                print("5: Custom (enter hex code)")
                                color_option = input("\nSelect an option: ")

                                if color_option == "1":
                                    interface_color = "\033[94m"
                                elif color_option == "2":
                                    interface_color = "\033[92m"
                                elif color_option == "3":
                                    interface_color = "\033[93m"
                                elif color_option == "4":
                                    interface_color = "\033[91m"
                                elif color_option == "5":
                                    hex_color = input("\nEnter hex color code (e.g., #00FF00): ")
                                    interface_color = f"\033[38;2;{int(hex_color[1:3], 16)};{int(hex_color[3:5], 16)};{int(hex_color[5:7], 16)}m"
                                else:
                                    print("\033[91mUnknown option. Please select a valid option.")
                                print(f"\033[92mInterface color set to: {interface_color}")
                            elif interface_option == "3":
                                break
                            else:
                                print("\033[91mUnknown option. Please select a valid option.")
                            input("\nPress Enter to continue...")

                    elif sub_option == "2":
                        while True:
                            if clear_screen:
                                clear_terminal()
                            print(interface_color)
                            print("\nQuality Settings")
                            print("1. Set AAC quality (default: 127)")
                            print("2. Set AAC bitrate (default: 256000)")
                            print("3. Set AAC strategy (default: 0 - CBR)")
                            print("4. Back to settings menu")
                            quality_option = input("\nSelect an option: ")

                            if quality_option == "1":
                                print("\033[93m")
                                print("AAC Quality (0-127):")
                                print("0: Lowest quality, smallest file size")
                                print("127: Highest quality, largest file size (default)")
                                try:
                                    quality = int(input("\nEnter AAC quality (0-127): "))
                                    if quality < 0 or quality > 127:
                                        raise ValueError
                                    print(f"\033[92mAAC quality set to: {quality}")
                                except ValueError:
                                    print(f"\033[91mInvalid quality value. Please enter a number between 0 and 127.")
                            elif quality_option == "2":
                                print("\033[93m")
                                print("AAC Bitrate (in bits per second):")
                                print("Higher bitrate usually means better quality but larger file size.")
                                print("256000: Default bitrate (256kbps)")
                                try:
                                    bitrate = int(input("\nEnter AAC bitrate (in bits per second): "))
                                    if bitrate <= 0:
                                        raise ValueError
                                    print(f"\033[92mAAC bitrate set to: {bitrate}")
                                except ValueError:
                                    print(f"\033[91mInvalid bitrate value. Please enter a positive number.")
                            elif quality_option == "3":
                                print("\033[93m")
                                print("AAC Strategy:")
                                print("0: CBR (Constant Bit Rate) - Default")
                                print("1: ABR (Average Bit Rate)")
                                print("2: VBR constrained (Variable Bit Rate constrained)")
                                print("3: VBR (Variable Bit Rate)")
                                try:
                                    strategy = int(input("\nEnter AAC strategy (0: CBR, 1: ABR, 2: VBR constrained, 3: VBR): "))
                                    if strategy < 0 or strategy > 3:
                                        raise ValueError
                                    print(f"\033[92mAAC strategy set to: {strategy}")
                                except ValueError:
                                    print(f"\033[91mInvalid strategy value. Please enter a number between 0 and 3.")
                            elif quality_option == "4":
                                break
                            else:
                                print("\033[91mUnknown option. Please select a valid option.")
                            input("\nPress Enter to continue...")

                    elif sub_option == "3":
                        settings = {
                            "quality": quality,
                            "bitrate": bitrate,
                            "strategy": strategy,
                            "clear_screen": clear_screen,
                            "interface_color": interface_color
                        }
                        save_settings(settings)
                    elif sub_option == "4":
                        break
                    else:
                        print("\033[91mUnknown option. Please select a valid option.")
                    input("\nPress Enter to continue...")

            elif option == "5":
                print("\033[93m")
                print(f"Current AAC quality: {quality}")
                print(f"Current AAC bitrate: {bitrate}")
                print(f"Current AAC strategy: {strategy}")
                print(f"Clear screen: {'On' if clear_screen else 'Off'}")
                print(f"Interface color: {color_to_readable(interface_color)}")
            elif option == "6":
                break
            else:
                print("\033[91mUnknown option. Please select a valid option.")
            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        print("\n\033[91mProgram interrupted by user. Exiting...\033[0m")

interactive_cli()
