from PyQt5 import QtWidgets
import sys


def window():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setGeometry(50,50,500,500)
    window.show()

    window.setWindowTitle("")
    app.exec()

window()