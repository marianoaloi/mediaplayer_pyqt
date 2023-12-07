import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton \
    , QStyle, QFileDialog , QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("C:/Users/maria/PycharmProjects/mediaplayer_pyqt/media.ui", self)

        self.initComponets();

    def initComponets(self):
        self.setWindowTitle("Hello MediaPlayer")
        self.video = QVideoWidget(self.videowidget)
        self.mediaplayer = QMediaPlayer(parent=self.videowidget, flags=QMediaPlayer.VideoSurface)
        self.mediaplayer.setVideoOutput(self.video)
        vbox = QVBoxLayout()
        vbox.addWidget(self.video)
        self.videowidget.setLayout(vbox)
        self.video.show()

        self.mediaplayer.durationChanged.connect(self.durationChange)
        self.mediaplayer.positionChanged.connect(self.positionChange)
        self.mediaplayer.stateChanged.connect(self.stateChanged)


        # self.play_pause = QPushButton()
        self.play_pause.setEnabled(False)
        self.play_pause.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_pause.clicked.connect(self.playPauseVideo)

        self.actionOpen.triggered.connect(self.openFile)

        self.videoSlider.setRange(0,0)
        self.videoSlider.sliderMoved.connect(self.setPosition)

    def stateChanged(self):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.play_pause.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_pause.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def positionChange(self,position):
        self.videoSlider.setValue(position)
        self.time.setPlainText(self.convertMillis(position))


    def durationChange(self,duration):
        self.videoSlider.setRange(0,duration)

    def setPosition(self,pos):
        self.mediaplayer.setPosition(int(pos))

    def openFile(self):
        fDialog = QFileDialog()
        fDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.mediaFile = fDialog.getOpenFileName(caption="Open Mediafile", filter=
                                                 "Video (*.mp4,*.avi,*.mkv);;Audio (*.mp3);;All Files (*.*)")
        if (self.mediaFile):
            self.mediaFile=self.mediaFile[0]
            self.mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.mediaFile)))
            self.mediaplayer.setPosition(0)
            self.mediaplayer.play()
            self.play_pause.setEnabled(True)
            self.videoFileLabel.setText(self.mediaFile)

    def playPauseVideo(self):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()
        else:
            self.mediaplayer.play()

    def convertMillis(self,millis:int):
        seconds=(millis/1000)%60
        minutes=(millis/(1000*60))%60
        hours=(millis/(1000*60*60))%24
        return '{0:02d}:{1:02d}:{2:02d}'.format(int(hours),int(minutes), int(seconds))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    winMediaPlayer = MediaPlayer()
    winMediaPlayer.show()
    sys.exit(app.exec())
