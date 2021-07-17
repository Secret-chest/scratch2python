import sys
from PySide6 import QtWidgets
# from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        outerLayout = QVBoxLayout()
        layout = QGridLayout()
        main = QWidget(self)
        self.setLayout(outerLayout)
        main.setLayout(layout)
        main.setObjectName("main")
        self.setCentralWidget(main)
        toolbar = QWidget(self)
        toolbar.setObjectName("toolbar")
        outerLayout.addWidget(toolbar)
        outerLayout.addWidget(main)
        toolbar.setMaximumHeight(64)

        #
        # TODO
        #

        self.statusBar().hide()
        self.show()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.setObjectName("window")


# Material Design colors
primaryColor = "#1675d1"
secondaryColor = "#ccdb37"
onPrimary = "#ffffff"
onSecondary = "#000000"
errorColor = "#d50000"
onError = "#ffffff"
background = "#ffffff"
surface = "#ffffff"
onBackground = "#000000"
onSurface = "#000000"


style = """

* {
    font-family: Roboto, apple-system, "Segoe UI", Arial, sans-serif;
}
#main, #window {
    background: #FFFFFF;
    font-size: 16px;
    border: none;
}
#toolbar {
    background: #1675d1;
}
#toolbar QLabel {
    color: #FFFFFF;
    padding: 18px;
}
QWidget {
    border-width: 3px;
    border-style: solid;
    border-image: 
        linear-gradient(
            to top, 
            black, 
            white
        ) 1 100%;
}



"""

app.setStyleSheet(style)


def placeholder():
    print("Placeholder")


app.exec()
