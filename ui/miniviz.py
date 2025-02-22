

import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor

class MiniViz(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(80, 30)  
        self.num_bars = 10
        self.values = [0]*self.num_bars
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)
        self.timer.start(100)  

    def update_values(self):
       
        self.values = [random.randint(0, 30) for _ in range(self.num_bars)]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        bar_w = w // self.num_bars
        for i, val in enumerate(self.values):
            x = i * bar_w
            bar_h = val
            y = h - bar_h
            painter.fillRect(x, y, bar_w - 1, bar_h, QColor("#00FF00"))
