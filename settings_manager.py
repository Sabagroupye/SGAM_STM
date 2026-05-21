import json
import os
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "presets.json")
def load_all_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
def save_preset(name, data):
    presets = load_all_settings()
    presets[name] = data
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=4, ensure_ascii=False)
def delete_preset(name):
    presets = load_all_settings()
    if name in presets:
        del presets[name]
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=4, ensure_ascii=False)