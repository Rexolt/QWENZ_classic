#!/usr/bin/env python
import os
import sys

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def check_required_files(file_list):
   
    missing = []
    for f in file_list:
      
        if not os.path.exists(resource_path(f)):
            missing.append(f)
    return missing

def main():
    
    required_files = [
        "resources/skins/classic.qss",
        "resources/fonts/W95FA.otf",
        "resources/icons/qwicon.png",
        "resources/icons/play.png",
        "resources/icons/pause.png",
        "resources/icons/stop.png",
        "resources/icons/next.png",
        "resources/icons/prev.png",
        "resources/images/bgmin.png",
        
        "resources/user_config.json",
        "audio"  
    ]

    missing = check_required_files(required_files)
    if missing:
        print("Hiba: A következő fájl(ok)/mappa(k) hiányoznak:")
        for item in missing:
            print(" -", item)
        sys.exit(1)
    else:
        print("Minden szükséges fájl és mappa megtalálható.")

if __name__ == "__main__":
    main()
