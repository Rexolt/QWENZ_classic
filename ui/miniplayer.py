# ui/miniplayer.py

import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from ui.realviz import RealViz  # <-- importáljuk a realisztikus vizualizációs widgetet

class WinampMiniPlayer(QWidget):
    def __init__(self, audio_manager, parent=None):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(275, 130)
        self.background = QPixmap("resources/images/bgmin.png")  # ha van
        self._drag_pos = None
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)

    def init_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 8, 10, 8)
        self.setLayout(main_layout)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.label_info = QLabel("00:00")
        self.label_info.setStyleSheet("QLabel { color: #ffcc00; font-size: 10px; }")
        top_layout.addWidget(self.label_info)

        btn_close = QPushButton("X")
        btn_close.setFixedSize(20, 20)
        btn_close.setStyleSheet("QPushButton { background-color: #666; color: #fff; border: 1px solid #999; font-size: 10px; }")
        btn_close.clicked.connect(self.close)
        top_layout.addWidget(btn_close)

        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        icon_dir = "resources/icons/"
        btn_prev = QPushButton()
        btn_prev.setIcon(QIcon(os.path.join(icon_dir, "prev.png")))
        btn_prev.setFixedSize(28, 24)
        btn_prev.clicked.connect(self.audio_manager.previous_track)
        bottom_layout.addWidget(btn_prev)

        btn_play = QPushButton()
        btn_play.setIcon(QIcon(os.path.join(icon_dir, "play.png")))
        btn_play.setFixedSize(28, 24)
        btn_play.clicked.connect(self.audio_manager.play)
        bottom_layout.addWidget(btn_play)

        btn_pause = QPushButton()
        btn_pause.setIcon(QIcon(os.path.join(icon_dir, "pause.png")))
        btn_pause.setFixedSize(28, 24)
        btn_pause.clicked.connect(self.audio_manager.pause)
        bottom_layout.addWidget(btn_pause)

        btn_stop = QPushButton()
        btn_stop.setIcon(QIcon(os.path.join(icon_dir, "stop.png")))
        btn_stop.setFixedSize(28, 24)
        btn_stop.clicked.connect(self.audio_manager.stop)
        bottom_layout.addWidget(btn_stop)

        btn_next = QPushButton()
        btn_next.setIcon(QIcon(os.path.join(icon_dir, "next.png")))
        btn_next.setFixedSize(28, 24)
        btn_next.clicked.connect(self.audio_manager.next_track)
        bottom_layout.addWidget(btn_next)

        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(self.audio_manager.get_volume())
        self.slider_volume.setFixedSize(60, 20)
        self.slider_volume.valueChanged.connect(self.audio_manager.set_volume)
        bottom_layout.addWidget(self.slider_volume)

        # REALISZTIKUS VIZ. FFT
        # Közvetlen a QMediaPlayer-hez férünk a realviz osztályban
        self.viz_widget = RealViz(self.audio_manager.player)
        main_layout.addWidget(self.viz_widget)

    def update_info(self):
        pos_ms = self.audio_manager.player.position()
        pos_sec = pos_ms // 1000
        m, s = divmod(pos_sec, 60)
        time_str = f"{m:02d}:{s:02d}"
        self.label_info.setText(time_str)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            painter.drawPixmap(0, 0, self.background)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
