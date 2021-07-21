import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QHBoxLayout
from windows.start_window import StartWindow
from windows.plot_window import PlotWindow


class UI:
    def __init__(self, store_path):
        self.app = QApplication(sys.argv)
        self.store_path = store_path

        


        # start window
        self.start_window = StartWindow(self.store_path)
        self.start_window.finished.connect(self.goto_plot)
        self.start_window.show()

        

        sys.exit(self.app.exec_())

    def goto_plot(self):
        self.start_window.close()
        # plot window
        self.plot_window = PlotWindow(csv_path=self.store_path)
        self.plot_window.show()


if __name__ == '__main__':
    ui = UI(os.path.join(os.getcwd(), 'resources', 'CSV raw data'))


