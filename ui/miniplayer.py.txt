import os
import sys
import pygame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QSlider, QHBoxLayout,
    QVBoxLayout, QGraphicsDropShadowEffect, QStyle, QStyleOption
)
from ui.realviz_pygame import RealVizPygame
from audio.playback import AudioManagerPygame as AudioManager

# resource_path() függvény
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def add_3d_effect(button):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(8)
    shadow.setOffset(2, 2)
    shadow.setColor(QColor(0, 0, 0, 160))
    button.setGraphicsEffect(shadow)

class WinampMiniPlayer(QWidget):
    def __init__(self, audio_manager, parent=None):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self.current_track_file = None

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setFixedSize(480, 260)

        # Háttérkép beállítása
        bg_path = resource_path(os.path.join("resources", "images", "bgmin.png"))
        self.background = QPixmap(bg_path)
        if not self.background.isNull():
            self.background = self.background.scaled(self.size())
        else:
            self.background = QPixmap(self.size())
            self.background.fill(QColor("#2F3A3E"))

        # Stíluslap (ez marad)
        self.setStyleSheet("""
            WinampMiniPlayer {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3F4247, stop:1 #2C2F33
                );
                color: #FFFFFF;
                font-family: Arial, sans-serif;
            }
            QLabel#TitleLabel {
                font-size: 16px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QLabel#SubLabel {
                font-size: 12px;
                color: #CCCCCC;
            }
            QPushButton {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5E6B72, stop:1 #3B464D
                );
                border: 1px solid #2E3A40;
                border-radius: 8px;
                padding: 5px;
                color: #FFFFFF;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6E7B82, stop:1 #4B5860
                );
            }
            QPushButton:pressed {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3B464D, stop:1 #5E6B72
                );
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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.album_art_label = QLabel()
        self.album_art_label.setFixedSize(90, 90)
        default_art = QPixmap(resource_path(os.path.join("resources", "images", "album_art.jpg")))
        if default_art.isNull():
            default_art = QPixmap(90, 90)
            default_art.fill(QColor("#555555"))
        else:
            default_art = default_art.scaled(
                self.album_art_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        self.album_art_label.setPixmap(default_art)
        top_layout.addWidget(self.album_art_label)

        mid_layout = QVBoxLayout()
        top_layout.addLayout(mid_layout)

        self.label_title = QLabel("Cím")
        self.label_title.setObjectName("TitleLabel")
        self.label_sub = QLabel("Előadó")
        self.label_sub.setObjectName("SubLabel")
        mid_layout.addWidget(self.label_title)
        mid_layout.addWidget(self.label_sub)

        self.viz_widget = RealVizPygame(self.audio_manager)
        mid_layout.addWidget(self.viz_widget)

        right_layout = QVBoxLayout()
        top_layout.addLayout(right_layout)

        self.label_time = QLabel("00:00")
        font_time = QFont()
        font_time.setPointSize(14)
        font_time.setBold(True)
        self.label_time.setFont(font_time)
        self.label_time.setStyleSheet("color: #00FFC9;")
        right_layout.addWidget(self.label_time, alignment=Qt.AlignRight)

        self.btn_close = QPushButton("X")
        self.btn_close.setFixedSize(24, 24)
        self.btn_close.clicked.connect(self.close)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #444;
                border: none;
                border-radius: 12px;
                color: #fff;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        right_layout.addWidget(self.btn_close, alignment=Qt.AlignRight)
        right_layout.addStretch()

        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)

        icon_dir = resource_path(os.path.join("resources", "icons"))
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

        volume_layout = QHBoxLayout()
        main_layout.addLayout(volume_layout)

        lbl_vol = QLabel("Hangerő:")
        lbl_vol.setStyleSheet("color: #CCCCCC; font-size: 12px;")
        volume_layout.addWidget(lbl_vol)

        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(self.audio_manager.get_volume())
        self.slider_volume.valueChanged.connect(self.audio_manager.set_volume)
        volume_layout.addWidget(self.slider_volume)

    def update_info(self):
        self.update_metadata()
        pos_ms = pygame.mixer.music.get_pos()
        pos_sec = pos_ms // 1000 if pos_ms >= 0 else 0
        m, s = divmod(pos_sec, 60)
        time_str = f"{m:02d}:{s:02d}"
        self.label_time.setText(time_str)

    def update_metadata(self):
        current_file = self.audio_manager.get_current_track_file()
        if current_file and current_file != self.current_track_file:
            self.current_track_file = current_file
            title, artist, album_art = self.load_metadata(current_file)
            self.label_title.setText(title if title else os.path.basename(current_file))
            self.label_sub.setText(artist if artist else "Ismeretlen előadó")
            if album_art:
                pixmap = QPixmap()
                pixmap.loadFromData(album_art)
                pixmap = pixmap.scaled(
                    self.album_art_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.album_art_label.setPixmap(pixmap)
            else:
                default_art = QPixmap(resource_path(os.path.join("resources", "images", "album_art.jpg")))
                if default_art.isNull():
                    default_art = QPixmap(self.album_art_label.size())
                    default_art.fill(QColor("#555555"))
                else:
                    default_art = default_art.scaled(
                        self.album_art_label.size(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                self.album_art_label.setPixmap(default_art)

    def load_metadata(self, file_path):
        from mutagen.id3 import ID3
        try:
            audio = ID3(file_path)
            title = audio.get('TIT2')
            artist = audio.get('TPE1')
            album_art = None
            apic_list = audio.getall("APIC")
            if apic_list:
                album_art = apic_list[0].data
            title_text = title.text[0] if title and title.text else None
            artist_text = artist.text[0] if artist and artist.text else None
            return title_text, artist_text, album_art
        except Exception as e:
            print("Metadata load error:", e)
            return None, None, None

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        if not self.background.isNull():
            scaled_bg = self.background.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
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
