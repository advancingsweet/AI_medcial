from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit
import sys

from component.MainWindow2 import MainWindow2
from component.ExprotWindow import ExportWindow

if __name__ == '__main__':

    app = QApplication([])

    window = MainWindow2()
    export=ExportWindow()

    window.Export.connect(export.Export_Slot)
    window.show()

    sys.exit(app.exec())
