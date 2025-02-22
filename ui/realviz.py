# ui/realviz.py

import numpy as np
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtMultimedia import QAudioProbe, QAudioBuffer

class RealViz(QWidget):
    """
    Egy FFT-alapú vizualizáció, mely a QAudioProbe adataiból számítja a sávokat.
    """
    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.setFixedSize(150, 50)
        self.num_bins = 16
        self.amplitudes = np.zeros(self.num_bins)
        self.probe = QAudioProbe()
        self.probe.audioBufferProbed.connect(self.process_buffer)
        self.probe.setSource(self.player)  # A QMediaPlayer

    @pyqtSlot(QAudioBuffer)
    def process_buffer(self, audio_buffer):
        # Ha itt semmit nem kapunk, lehet a formátum nem támogatott
        fmt = audio_buffer.format()
        if not fmt.isValid():
            return

        # Példa: 16 bites, 2 csatornás, 44100 Hz formátum
        # Kiolvassuk a mintákat numpy array-be
        data_bytes = audio_buffer.data()
        sample_count = audio_buffer.frameCount()
        channel_count = fmt.channelCount()

        # sample_count × channel_count mintát jelenthet
        # Adott platformon a sampleType lehet int16, float stb.

        sample_type = fmt.sampleType()
        bits = fmt.sampleSize()    # 8, 16, 24, 32...
        sample_size = bits // 8

        # Itt feltételezzük, hogy 16 bites PCM (SignedInt), 2 csatorna
        # Ha float vagy 8 bites, külön kezelni kell
        
        if sample_type != fmt.SignedInt or sample_size != 2:
            # Túl lényegesen eltér? Vagy megpróbálhatjuk float konverziót
            return

        # Numpy array (int16) - "int16" 2 csatornára
        raw_arr = np.frombuffer(data_bytes, dtype=np.int16)
        
        # Ha sztereó, 2 csatorna, vegyük az átlagot (monósítás)
        if channel_count == 2:
            left = raw_arr[0::2]
            right = raw_arr[1::2]
            samples = 0.5*(left.astype(np.float32) + right.astype(np.float32))
        else:
            # Egyszerűsítve, 1 csatorna
            samples = raw_arr.astype(np.float32)

        # FFT (gyors Fourier-transzformáció)
        # Hogy ne legyen túl nagy a számítás, kiválasztunk egy kisebb chunkot
        # pl. 1024 mintát
        n = min(len(samples), 1024)
        windowed = samples[:n] * np.hanning(n)  # ablakolás
        fft_result = np.fft.rfft(windowed)
        magnitude = np.abs(fft_result)

        # A low freq a magnitude[1..], max freq a mintavétel/2
        # Binning: 16 sáv
        freqs = np.linspace(0, len(magnitude)-1, self.num_bins+1)
        new_amplitudes = []
        for i in range(self.num_bins):
            start_i = int(freqs[i])
            end_i = int(freqs[i+1])
            # sáv átlag
            avg_val = np.mean(magnitude[start_i:end_i+1])
            new_amplitudes.append(avg_val)

        self.amplitudes = np.array(new_amplitudes)
        # repaint
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        bar_w = w // self.num_bins
        # Normalizáljuk a sávokat
        # pl. a max amplitude-t egy fix értékre skálázzuk
        max_amp = 20000.0  # kb. tetszőleges skála
        for i, amp in enumerate(self.amplitudes):
            x = i*bar_w
            val = amp / max_amp
            if val > 1.0:
                val = 1.0
            bar_h = val * h
            y = h - bar_h
            ix = int(x+1)
        iy = int(y)
        iw = int(bar_w - 2)
        ih = int(bar_h)
        painter.fillRect(ix, iy, iw, ih, QColor("#00FF00"))

