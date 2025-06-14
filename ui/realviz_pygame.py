import numpy as np
import os
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QStyle, QStyleOption
import pygame
from audio.playback import AudioManagerPygame as AudioManager

CHUNK = 1024
RATE = 44100

class RealVizPygame(QWidget):
    def __init__(self, audio_manager, parent=None):
        super().__init__(parent)
        self.audio_manager = audio_manager
        self.setFixedSize(200, 80)
        self.num_bins = 16
        self.CHUNK = CHUNK
        self.RATE = RATE
        self.amplitudes = np.zeros(self.num_bins)
        self.audio_samples = None

        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=self.RATE)

        self.load_audio_samples()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visualization)
        self.timer.start(50)

    def load_audio_samples(self):
        file_path = self.audio_manager.get_current_track_file()
        if not file_path:
            print("Nincs érvényes track fájl a vizualizációhoz.")
            return
        try:
            sound = pygame.mixer.Sound(file_path)
            arr = pygame.sndarray.array(sound)
            if arr.ndim > 1 and arr.shape[1] > 1:
                arr = arr.mean(axis=1)
            arr = arr.astype(np.float32) / 32768.0
            self.audio_samples = arr
            print("Audio samples betöltve, sample count:", len(arr))
        except Exception as e:
            print("Hiba az audio samples betöltésekor:", e)

    def update_visualization(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0 or self.audio_samples is None:
            return
        pos_samples = int((pos_ms / 1000.0) * self.RATE)
        if pos_samples + self.CHUNK > len(self.audio_samples):
            return
        chunk = self.audio_samples[pos_samples:pos_samples + self.CHUNK]
        window = np.hanning(len(chunk))
        windowed = chunk * window
        fft_result = np.fft.rfft(windowed)
        magnitude = np.abs(fft_result)

        freqs = np.linspace(0, len(magnitude) - 1, self.num_bins + 1)
        new_amplitudes = []
        for i in range(self.num_bins):
            start_i = int(freqs[i])
            end_i = int(freqs[i+1])
            if end_i - start_i > 0:
                avg_val = np.mean(magnitude[start_i:end_i])
            else:
                avg_val = 0
            new_amplitudes.append(avg_val)
        self.amplitudes = np.array(new_amplitudes)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#000000"))  # Fekete háttér

        w = self.width()
        h = self.height()
        bar_w = w // self.num_bins
        max_amp = 0.5

        painter.setPen(QPen(QColor("#00FF00"), 1))  # Zöld sávok
        painter.setBrush(QColor("#00FF00"))

        for i, amp in enumerate(self.amplitudes):
            x = i * bar_w
            val = amp / max_amp
            val = min(val, 1.0)
            bar_h = val * h
            y = h - bar_h
            painter.drawRect(int(x + 1), int(y), int(bar_w - 2), int(bar_h))

        opt = QStyleOption()
        opt.initFrom(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
