from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit, QRadioButton, QListView, QComboBox, \
    QPushButton, QFileDialog, QMessageBox
from PyQt5 import uic
from PyQt5 import QtGui
import sys
from os.path import expanduser
from pytube import YouTube, Playlist
import os


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("youtube_d.ui", self)
        self.url_lineEdit = self.findChild(QLineEdit, "url_lineEdit")
        self.format_mp3 = self.findChild(QRadioButton, "mp3_radioButton")
        self.format_mp4 = self.findChild(QRadioButton, "mp4_radioButton")
        self.video_radioButton = self.findChild(QRadioButton, "video_radioButton")
        self.playlist_radioButton = self.findChild(QRadioButton, "playlist_radioButton")
        self.resolution = self.findChild(QComboBox, "resolution_comboBox")
        self.resolution.addItem("240p")
        self.resolution.addItem("360p")
        self.resolution.addItem("480p")
        self.resolution.addItem("720p")
        self.resolution.addItem("1080p")
        self.directory_lineEdit = self.findChild(QLineEdit, "directory_lineEdit")
        self.browse_button = self.findChild(QPushButton, "browse_pushButton")
        self.listView = self.findChild(QListView, "listView")
        self.image_label = self.findChild(QLabel, "image_label")
        self.submit_button = self.findChild(QPushButton, "submit_pushButton")
        self.check_button = self.findChild(QPushButton, "check_pushButton")

        self.browse_button.clicked.connect(self.browse)
        self.submit_button.clicked.connect(self.download)
        self.check_button.clicked.connect(self.list_view_1)

        self.show()

    def browse(self):
        directory = QFileDialog.getExistingDirectory(None, "Select a folder:", expanduser(""))
        self.directory_lineEdit.setText(directory)

    def list_view_1(self):
        video_link = self.url_lineEdit.text()
        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)
        item = QtGui.QStandardItem(video_link)
        model.appendRow(item)
        if self.video_radioButton.isChecked():
            youtube_video = YouTube(video_link)
            v1 = "Downloading : {}".format(youtube_video.title)
            video_item = QtGui.QStandardItem(v1)
            model.appendRow(video_item)
        elif self.playlist_radioButton.isChecked():
            youtube_playlist = Playlist(video_link)
            for video in youtube_playlist.videos:
                s1 = "Downloading : {} with url : {}".format(video.title, video.watch_url)
                item = QtGui.QStandardItem(s1)
                model.appendRow(item)

    def download(self):
        video_link = self.url_lineEdit.text()
        model = QtGui.QStandardItemModel()
        if self.format_mp4.isChecked():
            playlist_link = video_link
            download_directory = self.directory_lineEdit.text()
            if self.video_radioButton.isChecked():
                youtube_video = YouTube(playlist_link)
                stream_playlist = youtube_video.streams.filter(res=self.resolution.currentText()).first()

                stream_playlist.download(download_directory)
                self.show_popup()
            elif self.playlist_radioButton.isChecked():
                youtube_playlist = Playlist(playlist_link)
                for video in youtube_playlist.videos:
                    video.streams.filter(type="video", progressive=True, file_extension="mp4").order_by(
                        "resolution").desc().first().download(download_directory)
                self.show_popup()
            else:
                item = QtGui.QStandardItem("Check Video Or Playlist!")
                model.appendRow(item)

        elif self.format_mp3.isChecked():
            playlist_link = video_link
            download_directory = self.directory_lineEdit.text()
            if self.video_radioButton.isChecked():
                youtube_video = YouTube(playlist_link)
                stream_playlist = youtube_video.streams.filter(only_audio=True).first()
                output_file = stream_playlist.download(download_directory)

                base, ext = os.path.splitext(output_file)
                new_file = base + ".mp3"
                os.rename(output_file, new_file)
                self.show_popup()

            elif self.playlist_radioButton.isChecked():
                playlist = Playlist(playlist_link)
                for video in playlist.videos:
                    audio = video.streams.get_audio_only()

                    output_file = audio.download(download_directory)

                    base, ext = os.path.splitext(output_file)
                    new_file = base + ".mp3"
                    os.rename(output_file, new_file)

                self.show_popup()
            else:
                item = QtGui.QStandardItem("Check Video Or Playlist!")
                model.appendRow(item)
        else:
            item = QtGui.QStandardItem("Check Mp3 or Mp4")
            model.appendRow(item)

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Download Completed!")
        msg.setText("Your video is ready!")
        msg.setIcon(QMessageBox.Information)

        msg.exec_()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
