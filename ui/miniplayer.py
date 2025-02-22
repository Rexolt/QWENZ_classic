import os
import pygame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QSlider, QHBoxLayout,
    QVBoxLayout, QGraphicsDropShadowEffect, QStyle, QStyleOption
)
from ui.realviz_pygame import RealVizPygame
from audio.playback import AudioManagerPygame as AudioManager

def add_3d_effect(button):
    """Alkalmaz egy drop shadow-t a gombra a 3D hatás érdekében."""
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(8)
    shadow.setOffset(2, 2)
    shadow.setColor(QColor(0, 0, 0, 160))
    button.setGraphicsEffect(shadow)

class WinampMiniPlayer(QWidget):
    """
    Egy mini lejátszó retro–modern kinézettel, amely 3D-s gombokat használ,
    integrálva van a RealVizPygame FFT vizualizáció.
    """
    def __init__(self, audio_manager, parent=None):
        super().__init__(parent)
        self.audio_manager = audio_manager

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFixedSize(  430, 180)

       
        self.background = QPixmap("resources/images/bgmin.png")
        if not self.background.isNull():
            self.background = self.background.scaled(self.size())
        else:
            self.background = QPixmap(self.size())
            self.background.fill(QColor("#2F3A3E"))

        self.setStyleSheet("""
            WinampMiniPlayer {
                background-color: #2F3A3E;
                color: #FFFFFF;
                font-family: Arial, sans-serif;
            }
            QLabel#TitleLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLabel#SubLabel {
                font-size: 11px;
                color: #aaaaaa;
            }
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #5E6B72, stop:1 #3B464D);
                border: 1px solid #2E3A40;
                border-radius: 8px;
                padding: 5px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #6E7B82, stop:1 #4B5860);
            }
            QPushButton:pressed {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #3B464D, stop:1 #5E6B72);
                border-style: inset;
            }
            QSlider::groove:horizontal {
                border: 1px solid #777;
                height: 4px;
                background: #444;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                border: 1px solid #777;
                width: 10px;
                margin: -5px 0;
                border-radius: 5px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        self._drag_pos = None
        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_info)
        self.timer.start(500)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        
        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(80, 80)
        album_pixmap = QPixmap("resources/images/album_art.jpg")
        if album_pixmap.isNull():
            album_pixmap = QPixmap(80, 80)
            album_pixmap.fill(QColor("#555555"))
        else:
            album_pixmap = album_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.album_art_label.setPixmap(album_pixmap)
        main_layout.addWidget(self.album_art_label)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(5)
        main_layout.addLayout(right_layout)

        self.label_title = QLabel("Retro Track Title")
        self.label_title.setObjectName("TitleLabel")
        self.label_sub = QLabel("Artist / Info")
        self.label_sub.setObjectName("SubLabel")
        right_layout.addWidget(self.label_title)
        right_layout.addWidget(self.label_sub)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(5)
        icon_dir = "resources/icons/"

        btn_prev = QPushButton()
        btn_prev.setIcon(QIcon(os.path.join(icon_dir, "prev.png")))
        btn_prev.clicked.connect(self.audio_manager.previous_track)
        add_3d_effect(btn_prev)
        controls_layout.addWidget(btn_prev)

        btn_play = QPushButton()
        btn_play.setIcon(QIcon(os.path.join(icon_dir, "play.png")))
        btn_play.clicked.connect(self.audio_manager.play)
        add_3d_effect(btn_play)
        controls_layout.addWidget(btn_play)

        btn_pause = QPushButton()
        btn_pause.setIcon(QIcon(os.path.join(icon_dir, "pause.png")))
        btn_pause.clicked.connect(self.audio_manager.pause)
        add_3d_effect(btn_pause)
        controls_layout.addWidget(btn_pause)

        btn_stop = QPushButton()
        btn_stop.setIcon(QIcon(os.path.join(icon_dir, "stop.png")))
        btn_stop.clicked.connect(self.audio_manager.stop)
        add_3d_effect(btn_stop)
        controls_layout.addWidget(btn_stop)

        btn_next = QPushButton()
        btn_next.setIcon(QIcon(os.path.join(icon_dir, "next.png")))
        btn_next.clicked.connect(self.audio_manager.next_track)
        add_3d_effect(btn_next)
        controls_layout.addWidget(btn_next)

        self.label_time = QLabel("00:00")
        self.label_time.setStyleSheet("font-size: 12px;")
        controls_layout.addWidget(self.label_time)

        right_layout.addLayout(controls_layout)

        self.viz_widget = RealVizPygame(self.audio_manager)
        right_layout.addWidget(self.viz_widget)

        slider_layout = QHBoxLayout()
        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(self.audio_manager.get_volume())
        self.slider_volume.valueChanged.connect(self.audio_manager.set_volume)
        slider_layout.addWidget(self.slider_volume)
        right_layout.addLayout(slider_layout)

        self.btn_close = QPushButton("X")
        self.btn_close.setFixedSize(20, 20)
        self.btn_close.clicked.connect(self.close)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #444;
                border: none;
                border-radius: 10px;
                color: #fff;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(self.btn_close)
        close_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(close_layout)

    def update_info(self):
        pos_ms = pygame.mixer.music.get_pos()
        pos_sec = pos_ms // 1000 if pos_ms >= 0 else 0
        m, s = divmod(pos_sec, 60)
        time_str = f"{m:02d}:{s:02d}"
        self.label_time.setText(time_str)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        if not self.background.isNull():
            scaled_bg = self.background.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_bg)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_drag_pos") and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
