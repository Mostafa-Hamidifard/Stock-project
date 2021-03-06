from detection.filter_detection import StockFilter
from detection.trend_detection import detect_trend
from Indicator.simple import Simple
from Indicator.normalize import Normalize
from Indicator.bbolinger import BBolinger
from Indicator.moving_average import MovingAverage
from Indicator.macd import MACD
from get import ExtractCompaniesFeatures
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
import matplotlib
from pdf import PDF
matplotlib.use("Qt5Agg")


Form1 = uic.loadUiType(os.path.join(
    os.getcwd(), 'resources', 'plot_window.ui'))[0]


class PlotWindow(Form1, QMainWindow):
    def __init__(self, csv_path):
        Form1.__init__(self)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.csv_path = csv_path

        self.raw_data = ExtractCompaniesFeatures(self.csv_path)
        company_names = self.raw_data.get_company_names()
        company_typename = ["<FIRST>", "<HIGH>", "<LOW>", "<CLOSE>",
                            "<VALUE>", "<VOL>", "<OPENINT>", "<OPEN>", "<LAST>"]

        for name in company_names:
            self.combobox_companyname.addItem(name)

        for typename in company_typename:
            self.combobox_typeName.addItem(typename)

        self.fig = Figure(dpi=150, edgecolor='k')
        self.ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        self.canvas = FigureCanvas(self.fig)
        self.navi = NavigationToolbar(self.canvas, self)
        plot_layout = QVBoxLayout(self.plot_widget)
        plot_layout.addWidget(self.canvas)
        plot_layout.addWidget(self.navi)

        self.movingaverage_rate.setValidator(QIntValidator(1, 999))
        self.macd_slow.setValidator(QIntValidator(1, 999))
        self.macd_fast.setValidator(QIntValidator(1, 999))
        self.macd_smooth.setValidator(QIntValidator(1, 999))
        self.bb_rate.setValidator(QIntValidator(1, 999))
        self.bb_mult.setValidator(QIntValidator(1, 999))
        self.lineEdit_trend.setValidator(QIntValidator(1, 999))

        self.combobox_companyname.currentTextChanged.connect(
            self.combobox_companyname_changed)
        self.combobox_typeName.currentTextChanged.connect(
            self.combobox_typename_changed)
        self.simple_checkbox.stateChanged.connect(self.checkbox_change)
        self.normalize_checkbox.stateChanged.connect(self.checkbox_change)
        self.bb_checkbox.stateChanged.connect(self.checkbox_change)
        self.macd_checkbox.stateChanged.connect(self.checkbox_change)
        self.movingaverage_checkbox.stateChanged.connect(self.checkbox_change)
        self.movingaverage_rate.textEdited.connect(self.lineEdit_changed)
        self.macd_slow.textEdited.connect(self.lineEdit_changed)
        self.macd_fast.textEdited.connect(self.lineEdit_changed)
        self.macd_smooth.textEdited.connect(self.lineEdit_changed)
        self.bb_rate.textEdited.connect(self.lineEdit_changed)
        self.bb_mult.textEdited.connect(self.lineEdit_changed)
        self.pushButton_trend.clicked.connect(self.trend_clicked)
        self.pushButton_filter.clicked.connect(self.filter_clicked)
        self.pushButton_saveas.clicked.connect(self.saveAs_clicked)

    def combobox_companyname_changed(self, str):
        self.plot()

    def combobox_typename_changed(self, str):
        self.plot()

    def checkbox_change(self, state):
        self.plot()

    def lineEdit_changed(self, text):
        self.plot()

    def trend_clicked(self):
        fromthis = int(self.lineEdit_trend.text()
                       ) if self.lineEdit_trend.text() != '' else -1
        if fromthis == -1:
            self.label_trend.setText("no status")
            QMessageBox.critical(self, "ERROR", "Please enter a valid number")
            return

        name = self.combobox_companyname.currentText()
        typename = self.combobox_typeName.currentText()
        if name == "" or typename == "":
            return
        company_data = self.raw_data.all_compnies_data[name]
        result, m, c = detect_trend(company_data, fromthis, -1, True, typename)
        self.label_trend.setText(result)

    def filter_clicked(self):
        filter_str = self.lineEdit_filter.text()
        name = self.combobox_companyname.currentText()
        typename = self.combobox_typeName.currentText()
        if name == "" or typename == "":
            return
        company_data = self.raw_data.all_compnies_data[name]
        try:
            filter = StockFilter(company_data, filter_str, typename)
            answer = "True" if filter.answer else "False"
            self.label_filter.setText(answer)
        except:
            QMessageBox.critical(
                self, "ERROR", "Please enter a valid expression")

    def saveAs_clicked(self):
        path = QFileDialog.getExistingDirectory(
            self, "select a file", os.getcwd())
        if path == "":
            QMessageBox.critical(self, "ERROR", "Please select a directory")
            return

        class mythread(QThread):

            def __init__(self, parent, all, path, fill):
                super(mythread, self).__init__(parent)
                self.all = all
                self.fill = fill
                self.path = path

            def run(self):
                pdf = PDF(self.all,
                          self.path, self.fill)
        all = list(self.raw_data.all_compnies_data.values())
        fill = self.lineEdit_filter.text()
        self.thread = mythread(self, all, path, fill)
        self.thread.start()

        print(path)

    def plot(self):
        name = self.combobox_companyname.currentText()
        typename = self.combobox_typeName.currentText()
        if name == "" or typename == "":
            return

        self.ax.legend([])
        self.ax.clear()
        company_data = self.raw_data.all_compnies_data[name]

        if self.simple_checkbox.isChecked():
            simple = Simple(company_data, typename)
            simple.plot(self.ax)

        if self.normalize_checkbox.isChecked():
            normal = Normalize(company_data, typename)
            normal.plot(self.ax)

        if self.bb_checkbox.isChecked():
            rate = int(self.bb_rate.text()
                       ) if self.bb_rate.text() != '' else 20
            mult = int(self.bb_mult.text()) if self.bb_mult.text() != '' else 2
            bb = BBolinger(company_data, typename, rate, mult)
            bb.plot(self.ax)

        if self.macd_checkbox.isChecked():
            slow = int(self.macd_slow.text()
                       ) if self.macd_slow.text() != '' else 26
            fast = int(self.macd_fast.text()
                       ) if self.macd_fast.text() != '' else 12
            smooth = int(self.macd_smooth.text()
                         ) if self.macd_smooth.text() != '' else 9
            mac = MACD(company_data, typename, slow, fast, smooth)
            mac.plot(self.ax)

        if self.movingaverage_checkbox.isChecked():
            rate = int(self.movingaverage_rate.text()
                       ) if self.movingaverage_rate.text() != '' else 12
            mv = MovingAverage(company_data, rate, typename)
            mv.plot(self.ax)

        self.ax.grid(b=True)
        self.fig.canvas.draw()
