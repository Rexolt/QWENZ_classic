import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from config.configmanager import ConfigManager
from ui.mainwindow import MainWindow

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    app = QApplication(sys.argv)
    
    config_file = resource_path(os.path.join("resources", "user_config.json"))
    config_manager = ConfigManager(config_file)
    config_manager.load_config()
    
    font_path = resource_path(os.path.join("resources", "fonts", "W95FA.otf"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id < 0:
        print("Nem sikerült betölteni a fontot:", font_path)
    else:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            app.setFont(QFont(families[0], 14))
    
    selected_style = config_manager.get_style()
    if selected_style == "Windows 95 Retro":
        qss_rel_path = os.path.join("resources", "skins", "win95_dark_v2.qss")
    elif selected_style == "Klasszikus":
        qss_rel_path = os.path.join("resources", "skins", "classic.qss")
    elif selected_style == "Sötét":
        qss_rel_path = os.path.join("resources", "skins", "modern.qss")
    else:
        qss_rel_path = os.path.join("resources", "skins", "win95_dark_v2.qss")
    
    qss_path = resource_path(qss_rel_path)
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()
        app.setStyleSheet(qss)
    except Exception as e:
        print("Hiba a stílus betöltésekor:", e)
   
    window = MainWindow(config_manager)
    window.show()
    
    exit_code = app.exec_()
    
    config_manager.save_config()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
