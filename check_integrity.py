import sys
import os
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QFontDatabase

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_file_exists_and_not_empty(file_path):
    if not os.path.exists(file_path):
        return False, "CRITICAL", "Does not exist."
    if os.path.getsize(file_path) == 0:
        return False, "CRITICAL", "File is empty."
    return True, "INFO", ""

def check_qss(file_path):
    exists, level, msg = check_file_exists_and_not_empty(file_path)
    if not exists:
        return False, level, msg
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return False, "CRITICAL", "QSS file is empty."
    except Exception as e:
        return False, "CRITICAL", f"Error reading QSS: {e}"
    return True, "INFO", ""

def check_font(file_path):
    exists, level, msg = check_file_exists_and_not_empty(file_path)
    if not exists:
        return False, level, msg
    font_id = QFontDatabase.addApplicationFont(file_path)
    if font_id == -1:
        return False, "CRITICAL", "Font loading failed."
    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        return False, "CRITICAL", "No font family found."
    return True, "INFO", ""

def check_image(file_path):
    exists, level, msg = check_file_exists_and_not_empty(file_path)
    if not exists:
        return False, level, msg
    pix = QPixmap(file_path)
    if pix.isNull():
        return False, "CRITICAL", "Image failed to load (corrupt)."
    return True, "INFO", ""

def check_config(file_path):
    exists, level, msg = check_file_exists_and_not_empty(file_path)
    if not exists:
        return False, level, msg
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception as e:
        return False, "CRITICAL", f"JSON load error: {e}"
    return True, "INFO", ""

def check_directory(dir_path, allowed_exts=None):
    if not os.path.exists(dir_path):
        return False, "CRITICAL", "Directory does not exist."
    if not os.path.isdir(dir_path):
        return False, "CRITICAL", "Not a directory."
    if allowed_exts:
        found = False
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith(allowed_exts):
                    found = True
                    break
            if found:
                break
        if not found:
            return False, "WARNING", f"No file with extensions {allowed_exts} found."
    return True, "INFO", ""

def main():
    app = QApplication(sys.argv)
    errors = []
    resources_to_check = {
        "QSS": ("resources/skins/classic.qss", check_qss),
        "Font": ("resources/fonts/W95FA.otf", check_font),
        "Main Icon": ("resources/icons/qwicon.png", check_image),
        "Play Icon": ("resources/icons/play.png", check_image),
        "Pause Icon": ("resources/icons/pause.png", check_image),
        "Stop Icon": ("resources/icons/stop.png", check_image),
        "Next Icon": ("resources/icons/next.png", check_image),
        "Prev Icon": ("resources/icons/prev.png", check_image),
        "Background Image": ("resources/images/bgmin.png", check_image),
        
        "Config": ("config/user_config.json", check_config),
        "Audio Folder": ("audio", lambda path: check_directory(path, allowed_exts=(".mp3", ".wav", ".flac", ".ogg", ".aac")))
    }
    print("Checking resources...")
    for name, (rel_path, check_func) in resources_to_check.items():
        abs_path = resource_path(rel_path)
        ok, level, msg = check_func(abs_path)
        if ok:
            print(f"[{level}] {name}: {rel_path}")
        else:
            print(f"[{level}] {name}: {rel_path} - {msg}")
            errors.append(f"{name} ({rel_path}): {msg}")
    if errors:
        print("\nErrors found:")
        for err in errors:
            print(" -", err)
        sys.exit(1)
    else:
        print("\nAll required resources are present and valid.")

if __name__ == "__main__":
    main()
