#imports
import os
from PyQt6.QtWidgets import QWidget,QApplication,QLabel,QPushButton,QListWidget,QFileDialog,QSlider,QVBoxLayout,QHBoxLayout
from PyQt6.QtCore import Qt,QUrl,QTime
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput

#My App
class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setting()
        self.initUi()
        self.event_handler()


    # Setttings
    def setting(self):
        self.setWindowTitle("Audio App")
        self.setGeometry(800,500,600,300)


    # Design
    def initUi(self):
        self.title = QLabel("Audio Adjuster")
        self.file_list = QListWidget()
        self.btn_opn = QPushButton("Choose a File")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_resume = QPushButton("Resume")
        self.btn_rst = QPushButton("Reset")

        #Deactivate button
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_rst.setDisabled(True)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(150)
        self.slider.setValue(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)

        self.slider_txt = QLabel("Speed: 100x")
        self.slider_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_txt)
        slider_layout.addWidget(self.slider)

        # Layout
        self.master=QVBoxLayout()
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        self.master.addWidget(self.title)
        self.master.addLayout(slider_layout)

        col1.addWidget(self.file_list)
        col2.addWidget(self.btn_opn)
        col2.addWidget(self.btn_play)
        col2.addWidget(self.btn_pause)
        col2.addWidget(self.btn_resume)
        col2.addWidget(self.btn_rst)

        row.addLayout(col1)
        row.addLayout(col2)

        self.master.addLayout(row)

        self.setLayout(self.master)


    # Even Handler
    def event_handler(self):
        self.slider.valueChanged.connect(self.update_slider)
        self.btn_opn.clicked.connect(self.open_file)

    #Funtionalities
        #Change slider speed label
    def update_slider(self):
        speed = self.slider.value()/100
        self.slider_txt.setText(f"Speed: {speed:.2f}x")

    def open_file(self):
        path = QFileDialog.getExistingDirectory(self,"Select Folder")

        if path:
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3"): # or wav and ogg
                    self.file_list.addItem(file_name)

        else:
            file, _ = QFileDialog.getOpenFileName(self, "Select File",filter="Audio Files (*.mp3)")
            if file:
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))
#Boiler Plate
if __name__ == "__main__":
    app = QApplication([])
    main=AudioApp()
    main.show()
    app.exec()