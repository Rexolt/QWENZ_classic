from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent

class AudioManager:
    def __init__(self):
        self.playlist = QMediaPlaylist()
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
        self.player.setVolume(50)

    def add_track(self, path):
        media = QMediaContent(QUrl.fromLocalFile(path))
        self.playlist.addMedia(media)

    def remove_track(self, index):
        self.playlist.removeMedia(index)

    def set_current_index(self, index):
        self.playlist.setCurrentIndex(index)

    def current_index(self):
        return self.playlist.currentIndex()

    def media_count(self):
        return self.playlist.mediaCount()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_playing(self):
        return self.player.state() == QMediaPlayer.PlayingState

    def is_stopped(self):
        return self.player.state() == QMediaPlayer.StoppedState

    def next_track(self):
        i = self.playlist.currentIndex()
        if i < self.playlist.mediaCount() - 1:
            self.playlist.setCurrentIndex(i + 1)
        else:
            self.playlist.setCurrentIndex(0)
        self.play()

    def previous_track(self):
        i = self.playlist.currentIndex()
        if i > 0:
            self.playlist.setCurrentIndex(i - 1)
        else:
            self.playlist.setCurrentIndex(self.playlist.mediaCount() - 1)
        self.play()

    def shuffle_on(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.Random)

    def shuffle_off(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)

    def repeat_on(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

    def repeat_off(self):
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)

    def set_volume(self, value):
        self.player.setVolume(value)

    def get_volume(self):
        return self.player.volume()
