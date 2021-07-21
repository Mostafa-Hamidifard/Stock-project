import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from PyQt5 import uic
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from get import ExtractCompaniesFeatures


Form1 = uic.loadUiType(os.path.join(os.getcwd(), 'resources', 'plot_window.ui'))[0]
class PlotWindow(Form1, QMainWindow):
    def __init__(self, csv_path):
        Form1.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.csv_path = csv_path

        self.combobox_companyname.currentTextChanged.connect(self.combobox_companyname_changed)
        self.combobox_typeName.currentTextChanged.connect(self.combobox_typename_changed)

        inst = ExtractCompaniesFeatures(self.csv_path)
        company_names = inst.get_company_names()
        company_typename = ["<FIRST>","<HIGH>","<LOW>","<CLOSE>","<VALUE>","<VOL>","<OPENINT>","<PER>","<OPEN>","<LAST>"]


        for name in company_names:
            self.combobox_companyname.addItem(name)
        
        for typename in company_typename:
            self.combobox_typeName.addItem(typename)
        

        self.fig = Figure()
        self.ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.canvas = FigureCanvas(self.fig)
        self.navi = NavigationToolbar(self.canvas, self)
        plot_layout = QVBoxLayout(self.plot_widget)
        plot_layout.addWidget(self.canvas)
        plot_layout.addWidget(self.navi)
        self.ax.plot([1, 2, 3], [1, 2, 3])
        self.fig.canvas.draw()
        

    def combobox_companyname_changed(self, str):
        print(str)
    
    def combobox_typename_changed(self, str):
        print(str)