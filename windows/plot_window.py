import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QHBoxLayout
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from PyQt5 import uic

Form1 = uic.loadUiType(os.path.join(os.getcwd(), 'resources', 'plot_window.ui'))[0]
class PlotWindow(Form1, QMainWindow):
    def __init__(self, csv_path):
        Form1.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.combo_box.currentTextChanged.connect(self.combobox_changed)
        inst_names = ['gav', 'palang', 'shir', 'gorbe']
        for name in inst_names:
            self.combo_box.addItem(name)

    def combobox_changed(self, str):
        print(str)