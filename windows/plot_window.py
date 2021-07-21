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
from Indicator.macd import MACD
from Indicator.moving_average import MovingAverage
from Indicator.bbolinger import BBolinger


Form1 = uic.loadUiType(os.path.join(os.getcwd(), 'resources', 'plot_window.ui'))[0]
class PlotWindow(Form1, QMainWindow):
    def __init__(self, csv_path):
        Form1.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.csv_path = csv_path

        

        self.raw_data = ExtractCompaniesFeatures(self.csv_path)
        company_names = self.raw_data.get_company_names()
        company_typename = ["<FIRST>","<HIGH>","<LOW>","<CLOSE>","<VALUE>","<VOL>","<OPENINT>","<OPEN>","<LAST>"]


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

        self.combobox_companyname.currentTextChanged.connect(self.combobox_companyname_changed)
        self.combobox_typeName.currentTextChanged.connect(self.combobox_typename_changed)
        self.simple_checkbox.stateChanged.connect(self.checkbox_change)
        self.bb_checkbox.stateChanged.connect(self.checkbox_change)
        self.macd_checkbox.stateChanged.connect(self.checkbox_change)
        self.movingaverage_checkbox.stateChanged.connect(self.checkbox_change)
        

    def combobox_companyname_changed(self, str):
        self.plot()
    
    def combobox_typename_changed(self, str):
        self.plot()

    def checkbox_change(self, state):
        self.plot()

    
    def plot(self):


        name = self.combobox_companyname.currentText()
        typename = self.combobox_typeName.currentText()
        if name == "" or typename == "":
            return

        self.ax.legend([])
        self.ax.clear()
        company_data = self.raw_data.all_compnies_data[name]
        
        if self.simple_checkbox.isChecked():
            pass

        if self.bb_checkbox.isChecked():
            bb = BBolinger(company_data, typename)
            bb.plot(self.ax)

        if self.macd_checkbox.isChecked():
            mac = MACD(company_data, typename)
            mac.plot(self.ax)
        
        if self.movingaverage_checkbox.isChecked():
            mv = MovingAverage(company_data, 12, typename)
            mv.plot(self.ax)

        self.fig.canvas.draw()
        
