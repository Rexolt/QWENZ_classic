import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.mainwindow import MainWindow
from config.configmanager import ConfigManager
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFontDatabase, QFont

def main():
    app = QApplication(sys.argv)
    config_manager = ConfigManager("resources/user_config.json")
    config_manager.load_config()
    with open("resources/skins/classic.qss", "r", encoding="utf-8") as f:
        qss = f.read()
    app.setStyleSheet(qss)
    window = MainWindow(config_manager)
    window.show()
    code = app.exec_()
    config_manager.save_config()
    font_path = os.path.join("resources", "fonts", "W95FA.otf")  
    font_id = QFontDatabase.addApplicationFont(font_path)
    families = QFontDatabase.applicationFontFamilies(font_id)
    print("Betűcsaládok:", families)
    QFontDatabase.addApplicationFont("resources/fonts/W95FA.otf")
    with open("resources/skins/classic.qss", "r", encoding="utf-8") as f:
        qss = f.read()
    print("QSS length:", len(qss))
    app.setStyleSheet(qss)
    
   
    
    """
    font_path = os.path.join("resources", "fonts", "W95FA.otf")  
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id < 0:
        print("Nem sikerült betölteni az OTF fontot:", font_path)
    else:
       
        families = QFontDatabase.applicationFontFamilies(font_id)
        print("Betöltött fontcsalád(ok):", families)
        if families:
            
            loaded_font_name = families[0]
            
            app.setFont(QFont(loaded_font_name, 14))

    label = QLabel("Szöveg, ami már a betöltött OTF fontot használhatja.")
    label.show()
    
    
    sys.exit(code)
"""


  
if __name__ == "__main__":
    main()
