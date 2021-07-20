import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QHBoxLayout
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from PyQt5 import uic

from receiving_and_cleaning.receive_data import start_downloading_data_and_store


class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, input_file_path, store_file_path):
        QObject.__init__(self)
        self.input_file_path = input_file_path
        self.store_file_path = store_file_path

    def run(self):
        start_downloading_data_and_store(self.input_file_path, self.store_file_path)
        self.finished.emit()


Form2 = uic.loadUiType(os.path.join(os.getcwd(), 'resources', 'start_window.ui'))[0]
class StartWindow(Form2, QMainWindow):
    finished = pyqtSignal()
    def __init__(self, input_path, store_path):
        Form2.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # self.progress_bar.setOrientation()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.progress_bar.minimum())
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.progress_timeout)

        self.start.clicked.connect(self.start_clicked)

        self.thread = QThread()
        self.worker = Worker(input_path, store_path )
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.finished_download)

    def start_clicked(self):
        self.progress_timer.start(10)
        self.thread.start()

    def progress_timeout(self):
        a = self.progress_bar.value() + 1
        if a > self.progress_bar.maximum():
            a = 0
        self.progress_bar.setValue(a)

    def finished_download(self):
        self.progress_timer.stop()
        self.finished.emit()