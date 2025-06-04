from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton, QFrame, QComboBox
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, audio_manager, config_manager, parent=None):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self.config_manager = config_manager
        self.setWindowTitle("Beállítások (Retro)")

        layout = QVBoxLayout()
        self.setLayout(layout)

      
        f = QFrame()
        h = QHBoxLayout()
        f.setLayout(h)
        f.setStyleSheet("QFrame { border: 2px ridge #808080; background-color: #C0C0C0; }")
        layout.addWidget(f)

        self.eq_sliders = []
        eq_values = self.config_manager.get_eq_values()
        for i in range(5):
            s = QSlider(Qt.Vertical)
            s.setRange(-10, 10)
            s.setValue(eq_values[i])
            h.addWidget(s)
            self.eq_sliders.append(s)

       
        style_layout = QHBoxLayout()
        lbl_style = QLabel("Stílus:")
        self.styleComboBox = QComboBox()
        self.styleComboBox.addItem("Windows 95 Retro")
        self.styleComboBox.addItem("Klasszikus")
        self.styleComboBox.addItem("Sötét")
        style_layout.addWidget(lbl_style)
        style_layout.addWidget(self.styleComboBox)
        layout.addLayout(style_layout)

    
        self.chk_shuffle = QCheckBox("Shuffle")
        self.chk_shuffle.setChecked(self.config_manager.get_shuffle())
        self.chk_repeat = QCheckBox("Repeat")
        self.chk_repeat.setChecked(self.config_manager.get_repeat())
        layout.addWidget(self.chk_shuffle)
        layout.addWidget(self.chk_repeat)

       
        vol_layout = QHBoxLayout()
        lbl_vol = QLabel("Hangerő:")
        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(self.config_manager.get_volume())
        vol_layout.addWidget(lbl_vol)
        vol_layout.addWidget(self.slider_volume)
        layout.addLayout(vol_layout)

        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Mégse")
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

        self.slider_volume.valueChanged.connect(self.audio_manager.set_volume)

    def accept(self):
       
        if self.chk_shuffle.isChecked():
            self.audio_manager.shuffle_on()
            self.config_manager.set_shuffle(True)
        else:
            self.audio_manager.shuffle_off()
            self.config_manager.set_shuffle(False)

       
        if self.chk_repeat.isChecked():
            self.audio_manager.repeat_on()
            self.config_manager.set_repeat(True)
        else:
            self.audio_manager.repeat_off()
            self.config_manager.set_repeat(False)

        
        v = self.slider_volume.value()
        self.config_manager.set_volume(v)
        self.audio_manager.set_volume(v)

        
        eq_vals = [s.value() for s in self.eq_sliders]
        self.config_manager.set_eq_values(eq_vals)

        
        selected_style = self.styleComboBox.currentText()
        if selected_style == "Windows 95 Retro":
            qss_file = "resources/skins/win95_dark_v2.qss"
        elif selected_style == "Klasszikus":
            qss_file = "resources/skins/classic.qss"
        elif selected_style == "Sötét":
            qss_file = "resources/skins/modern.qss"
        else:
            qss_file = ""

        if qss_file:
            try:
                with open(qss_file, "r", encoding="utf-8") as f:
                    qss = f.read()
                    if self.parent():
                        self.parent().setStyleSheet(qss)
            except Exception as e:
                print("Hiba a stílus betöltésekor:", e)

        super().accept()
