from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QPushButton, QFrame
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
        f.setStyleSheet("QFrame { border: 1px solid #888; }")
        layout.addWidget(f)

        self.eq_sliders = []
        eq_values = self.config_manager.get_eq_values()
        for i in range(5):
            s = QSlider(Qt.Vertical)
            s.setRange(-10, 10)
            s.setValue(eq_values[i])
            h.addWidget(s)
            self.eq_sliders.append(s)

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

        super().accept()
