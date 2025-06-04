import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5.QtWidgets import QApplication, QWidget

from config.configmanager import ConfigManager
from ui.settingsdialog import SettingsDialog

class DummyAudio:
    def set_volume(self, v):
        pass
    def shuffle_on(self):
        pass
    def shuffle_off(self):
        pass
    def repeat_on(self):
        pass
    def repeat_off(self):
        pass

def main():
    app = QApplication(sys.argv)
    cm = ConfigManager('resources/user_config.json')
    cm.load_config()
    parent = QWidget()
    dlg = SettingsDialog(DummyAudio(), cm, parent)
    idx = dlg.styleComboBox.findText('Sötét')
    dlg.styleComboBox.setCurrentIndex(idx)
    dlg.accept()
    applied = 'background-color' in parent.styleSheet()
    print('APPLIED' if applied else 'NOT APPLIED')

if __name__ == '__main__':
    main()
