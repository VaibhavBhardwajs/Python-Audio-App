#imports
import os
from PyQt6.QtWidgets import QWidget,QApplication,QLabel,QPushButton,QListWidget,QFileDialog,QSlider,QVBoxLayout,QHBoxLayout
from PyQt6.QtCore import Qt,QUrl,QTime
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput

#My App
class AudioApp(QWidget):
    def __init__(self):
        super().__init__()


#Boiler Plate
if __name__ == "__main__":
    app = QApplication([])
    main=AudioApp()
    main.show()
    app.exec()