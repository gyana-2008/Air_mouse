import json
import os

class SettingsManager:
    def __init__(self):
        self.config_file = "config.json"
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return json.load(f)
        return {} # Return empty dict if file is missing

    def save_settings(self):
        with open(self.config_file, "w") as f:
            json.dump(self.settings, f, indent=4)
            
    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()