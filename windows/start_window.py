import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from PyQt5 import uic

from receiving_and_cleaning.receive_data import start_downloading_data_and_store


class Worker(QObject):
    finished = pyqtSignal(str)

    def __init__(self, input_file_path, store_file_path):
        QObject.__init__(self)
        self.input_file_path = input_file_path
        self.store_file_path = store_file_path

    def run(self):
        try:
            start_downloading_data_and_store(self.input_file_path, self.store_file_path)
            self.finished.emit("OK")
        
        except:
            self.finished.emit("ERROR")
           
        


Form2 = uic.loadUiType(os.path.join(os.getcwd(), 'resources', 'start_window.ui'))[0]
class StartWindow(Form2, QMainWindow):
    finished = pyqtSignal()
    def __init__(self, store_path):
        Form2.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.input_path = None
        self.store_path = store_path

        # background_path = os.path.join(os.getcwd(), "resources", "image.jpg")
        # stylesheet = 'background-image: url("{}"); background-position: center;'.format(background_path)
        # print(stylesheet)
        # self.centralWidget().setStyleSheet(stylesheet)

        # self.progress_bar.setOrientation()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(self.progress_bar.minimum())
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.progress_timeout)

        self.start.clicked.connect(self.start_clicked)
        self.browse.clicked.connect(self.browse_clicked)

        

    def start_clicked(self):
        if self.input_path is None:
            QMessageBox.critical(self, "ERROR", "Please select a file first")
            return

        self.thread = QThread()
        self.worker = Worker(self.input_path, self.store_path )
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.finished_download)

        self.progress_timer.start(10)
        self.start.setEnabled(False)
        self.thread.start()
    
    def browse_clicked(self):
        path = QFileDialog.getOpenFileName(self, "select a file", os.getcwd(), "text files (*.txt)")
        path = path[0]
        if path != "":
            self.browse_label.setText(os.path.basename(path))
            self.input_path = path
        else:
            self.input_path = None
            self.browse_label.setText("no file")


    def progress_timeout(self):
        a = self.progress_bar.value() + 1
        if a > self.progress_bar.maximum():
            a = 0
        self.progress_bar.setValue(a)

    def finished_download(self, res):
        self.progress_timer.stop()

        if res == "OK":
            self.finished.emit()
        else:
            # alert = QMessageBox()
            # alert.setStyleSheet("QMessageBox{background-color: #c4ff4d; border: 4px solid #1a6600; border-radius: 5px;} QPushButton{background-color: red; }")
            # alert.setText("Connection faild")
            # alert.setInformativeText("Plead try again")
            # alert.exec()
            QMessageBox.critical(self, "ERROR", "Please check your network connection and stock IDs")
            self.start.setEnabled(True)
            self.start.setText("Try Again")
