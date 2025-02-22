import json
import os

class ConfigManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {
            "volume": 50,
            "shuffle": False,
            "repeat": False,
            "eqValues": [0, 0, 0, 0, 0]
        }

    def load_config(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.data.update(loaded)
            except:
                pass

    def save_config(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except:
            pass

    def get_volume(self):
        return self.data.get("volume", 50)

    def set_volume(self, vol):
        self.data["volume"] = vol

    def get_shuffle(self):
        return self.data.get("shuffle", False)

    def set_shuffle(self, value):
        self.data["shuffle"] = value

    def get_repeat(self):
        return self.data.get("repeat", False)

    def set_repeat(self, value):
        self.data["repeat"] = value

    def get_eq_values(self):
        return self.data.get("eqValues", [0, 0, 0, 0, 0])

    def set_eq_values(self, eq_list):
        self.data["eqValues"] = eq_list
