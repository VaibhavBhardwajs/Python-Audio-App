#imports
import os
from PyQt6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

# My App
class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setting()
        self.initUi()
        self.event_handler()
        self.folder_path = None  # Store the folder path here
        self.style()

    # Settings
    def setting(self):
        self.setWindowTitle("Audio App")
        self.setGeometry(800, 500, 600, 300)

    # Design
    def initUi(self):
        self.title = QLabel("Audio Adjuster")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.file_list = QListWidget()
        self.btn_opn = QPushButton("Choose a Folder")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_resume = QPushButton("Resume")
        self.btn_rst = QPushButton("Reset")

        # Deactivate buttons initially
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
        self.slider_txt.setObjectName('speed')
        self.slider_txt.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_txt)
        slider_layout.addWidget(self.slider)

        # Layout
        self.master = QVBoxLayout()
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

        row.addLayout(col1,2)
        row.addLayout(col2,4)

        self.master.addLayout(row)

        self.setLayout(self.master)

        # Special Audio Classes from PyQt
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)

    # Event Handler
    def event_handler(self):
        self.slider.valueChanged.connect(self.update_slider)
        self.btn_opn.clicked.connect(self.open_file)
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_resume.clicked.connect(self.resume_audio)
        self.btn_rst.clicked.connect(self.reset_audio)

        # Automatically play the next song or loop the current song
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)


    # Styling
    def style(self):
        self.setStyleSheet("""
                            QWidget{
                            background-color: dark-gray;
                           }

                           QPushButton{
                            background-color: #5BB9C2;
                            padding: 15px;
                            border-radius:9px;
                            color:#333;
                           }

                           QPushButton:hover{
                            background-color: #1A4870;
                            color:#F9DBBA;
                           }

                            QPushButton:disabled{
                                background-color: #A0D4DA;  /* Lighter shade of the activated button */
                                color: #999;  /* Lighter text color */
                            }

                           QLabel{
                            color:#333;
                           }
                           #title{
                            font-family:Papyrus;
                            font-size:40px;
                            color:white;
                           }

                           #speed{
                            color:white;
                           }

                           QSlider{
                            margin-right: 15px;
                           }

                           QListWidget{
                            color:#333;
                            background-color: white;
                           }

                           

                            """)

    # Functionalities
    def update_slider(self):
        speed = self.slider.value() / 100
        self.slider_txt.setText(f"Speed: {speed:.2f}x")
        if self.media_player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia:
            self.media_player.setPlaybackRate(speed)  # Update playback speed in real-time

    def open_file(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if path:
            self.folder_path = path  # Store the folder path
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3"):  # or wav and ogg
                    self.file_list.addItem(file_name)

        else:
            file, _ = QFileDialog.getOpenFileName(self, "Select File", filter="Audio Files (*.mp3)")
            if file:
                self.folder_path = os.path.dirname(file)  # Store the file's folder path
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))

    def play_audio(self):
        if self.file_list.selectedItems() and self.folder_path:
            file_name = self.file_list.selectedItems()[0].text()
            file_path = os.path.join(self.folder_path, file_name)
            file_url = QUrl.fromLocalFile(file_path)

            self.media_player.setSource(file_url)
            self.media_player.setPlaybackRate(self.slider.value() / 100.0)
            self.media_player.play()

            # Ensure playback speed updates as the slider moves
            self.slider.valueChanged.connect(lambda: self.media_player.setPlaybackRate(self.slider.value() / 100.0))

            # Activate buttons
            self.btn_pause.setEnabled(True)
            self.btn_resume.setDisabled(True)
            self.btn_rst.setEnabled(True)
            self.btn_play.setDisabled(True)

    def pause_audio(self):
        self.media_player.pause()
        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)

    def resume_audio(self):
        self.media_player.play()
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)

    def reset_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop()

        self.media_player.setPosition(0)
        self.media_player.setPlaybackRate(self.slider.value() / 100.0)
        self.media_player.play()

        # Activate buttons
        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_rst.setDisabled(True)
        self.btn_play.setDisabled(True)

        QTimer.singleShot(100, lambda: self.btn_rst.setEnabled(True))

    def handle_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            # Check if there are more songs in the list
            current_index = self.file_list.currentRow()
            if current_index < self.file_list.count() - 1:
                self.file_list.setCurrentRow(current_index + 1)
                self.play_audio()  # Play the next song
            else:
                self.media_player.setPosition(0)  # Loop the current song
                self.media_player.play()

# Boilerplate
if __name__ == "__main__":
    app = QApplication([])
    main = AudioApp()
    main.show()
    app.exec()
