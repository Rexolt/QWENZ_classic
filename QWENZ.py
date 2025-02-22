import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from config.configmanager import ConfigManager
from ui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)

  
    config_manager = ConfigManager("resources/user_config.json")
    config_manager.load_config()

    
    font_path = os.path.join("resources", "fonts", "W95FA.otf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id < 0:
        print("Nem sikerült betölteni a fontot:", font_path)
    else:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            app.setFont(QFont(families[0], 14))

    
    qss_path = os.path.join("resources", "skins", "classic.qss")
    with open(qss_path, "r", encoding="utf-8") as f:
        qss = f.read()
    app.setStyleSheet(qss)

   
    window = MainWindow(config_manager)
    window.show()

    
    exit_code = app.exec_()

   
    config_manager.save_config()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
