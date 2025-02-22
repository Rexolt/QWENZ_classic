import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QFileDialog, QToolBar, QAction, QLabel, QSlider
)
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QIcon
from audio.playback import AudioManager
from ui.settingsdialog import SettingsDialog
from ui.miniplayer import WinampMiniPlayer

class MainWindow(QMainWindow):
    def __init__(self, config_manager):
        super().__init__()
        self.setWindowTitle("QWENZ")
        self.setGeometry(100, 100, 800, 600)
        self.mini_player = None

        self.config_manager = config_manager
        self.audio_manager = AudioManager()

        self.audio_manager.set_volume(self.config_manager.get_volume())
        if self.config_manager.get_shuffle():
            self.audio_manager.shuffle_on()
        if self.config_manager.get_repeat():
            self.audio_manager.repeat_on()

        self.create_menu()
        self.create_toolbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.lbl_banner = QLabel("QWENZ")
        self.lbl_banner.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_banner)

        self.playlist_widget = QListWidget()
        self.playlist_widget.currentRowChanged.connect(self.on_select_track)
        main_layout.addWidget(self.playlist_widget, stretch=1)

        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        self.btn_add = QPushButton("Hozzáadás")
        self.btn_remove = QPushButton("Törlés")
        bottom_layout.addWidget(self.btn_add)
        bottom_layout.addWidget(self.btn_remove)

        self.btn_add.clicked.connect(self.add_songs)
        self.btn_remove.clicked.connect(self.remove_song)

        self.lbl_status = QLabel("Nincs lejátszás")
        self.lbl_status.setStyleSheet("QLabel { border: 1px solid #777; background-color: #333; padding: 4px; }")
        main_layout.addWidget(self.lbl_status)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(1000)

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Fájl")
        action_open = QAction("Megnyitás...", self)
        action_open.triggered.connect(self.add_songs)
        file_menu.addAction(action_open)

        file_menu.addSeparator()
        action_exit = QAction("Kilépés", self)
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        action_miniplayer = QAction("Mini lejátszó", self)
        action_miniplayer.triggered.connect(self.show_miniplayer)
        file_menu.addAction(action_miniplayer)

        settings_menu = menubar.addMenu("Beállítások")
        action_settings = QAction("Beállítások megnyitása", self)
        action_settings.triggered.connect(self.open_settings)
        settings_menu.addAction(action_settings)

    def create_toolbar(self):
        self.toolbar = QToolBar("Playback Controls")
        self.toolbar.setAllowedAreas(Qt.AllToolBarAreas)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self.toolbar.installEventFilter(self)

        icon_dir = "resources/icons/"
        action_backward = QAction(QIcon(os.path.join(icon_dir, "rew.png")), "Visszatekerés", self)
        action_prev = QAction(QIcon(os.path.join(icon_dir, "prev.png")), "Előző", self)
        action_play = QAction(QIcon(os.path.join(icon_dir, "play.png")), "Lejátszás", self)
        action_pause = QAction(QIcon(os.path.join(icon_dir, "pause.png")), "Szünet", self)
        action_stop = QAction(QIcon(os.path.join(icon_dir, "stop.png")), "Stop", self)
        action_next = QAction(QIcon(os.path.join(icon_dir, "next.png")), "Következő", self)
        action_forward = QAction(QIcon(os.path.join(icon_dir, "for.png")), "Előretekerés", self)

        action_backward.triggered.connect(self.seek_backward)
        action_prev.triggered.connect(self.audio_manager.previous_track)
        action_play.triggered.connect(self.audio_manager.play)
        action_pause.triggered.connect(self.audio_manager.pause)
        action_stop.triggered.connect(self.audio_manager.stop)
        action_next.triggered.connect(self.audio_manager.next_track)
        action_forward.triggered.connect(self.seek_forward)

        self.toolbar.addAction(action_backward)
        self.toolbar.addAction(action_prev)
        self.toolbar.addAction(action_play)
        self.toolbar.addAction(action_pause)
        self.toolbar.addAction(action_stop)
        self.toolbar.addAction(action_next)
        self.toolbar.addAction(action_forward)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.audio_manager.get_volume())
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.toolbar.addWidget(self.volume_slider)

    def eventFilter(self, obj, event):
        if obj == self.toolbar and event.type() in (QEvent.Move, QEvent.Resize, QEvent.LayoutRequest):
            area = self.toolBarArea(self.toolbar)
            if area in (Qt.LeftToolBarArea, Qt.RightToolBarArea):
                self.volume_slider.setOrientation(Qt.Vertical)
            else:
                self.volume_slider.setOrientation(Qt.Horizontal)
        return super().eventFilter(obj, event)

    def seek_forward(self):
        current_ms = self.audio_manager.player.position()
        new_ms = current_ms + 5000
        self.audio_manager.player.setPosition(new_ms)

    def seek_backward(self):
        current_ms = self.audio_manager.player.position()
        new_ms = max(current_ms - 5000, 0)
        self.audio_manager.player.setPosition(new_ms)

    def on_volume_changed(self, value):
        self.audio_manager.set_volume(value)

    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Zene hozzáadása", "",
                                                "Audio files (*.mp3 *.wav *.flac *.ogg *.aac)")
        if files:
            old_count = self.audio_manager.media_count()
            for f in files:
                self.audio_manager.add_track(f)
                self.playlist_widget.addItem(os.path.basename(f))
            if old_count == 0 and self.audio_manager.media_count() > 0:
                self.audio_manager.set_current_index(0)
                self.audio_manager.play()

    def remove_song(self):
        idx = self.playlist_widget.currentRow()
        if idx >= 0:
            self.audio_manager.remove_track(idx)
            self.playlist_widget.takeItem(idx)

    def on_select_track(self, index):
        if index >= 0:
            self.audio_manager.set_current_index(index)
            self.audio_manager.play()

    def update_status(self):
        idx = self.audio_manager.current_index()
        if idx < 0 or idx >= self.playlist_widget.count():
            self.lbl_status.setText("Nincs lejátszás")
            return
        title = self.playlist_widget.item(idx).text()
        state_str = "Lejátszás" if self.audio_manager.is_playing() else "Szünet / Stop"
        self.lbl_status.setText(f"{idx+1}. {title} - [{state_str}]")

    def open_settings(self):
        dlg = SettingsDialog(self.audio_manager, self.config_manager, self)
        dlg.exec_()

    def show_miniplayer(self):
        if not self.mini_player:
            self.mini_player = WinampMiniPlayer(self.audio_manager)
        self.mini_player.show()
        self.mini_player.raise_()
