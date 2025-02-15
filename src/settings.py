import json
import os

SETTINGS_FILE = "settings.json"

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f)
        print("\033[92mSettings saved successfully.")
    except Exception as e:
        print(f"\033[91mError saving settings: {e}")

def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            print("\033[92mSettings loaded successfully.")
            return settings
        else:
            return {}
    except Exception as e:
        print(f"\033[91mError loading settings: {e}")
        return {}
