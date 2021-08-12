import sys
from PySide6 import QtWidgets
# from PySide2 import QtWidgets
# from PyQt5 import QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *
import requests

app = QApplication()
window = QWidget()
layout = QVBoxLayout(window)
menuBar = QMenuBar()
layout.addWidget(menuBar)
toolsMenu = menuBar.addMenu("&Tools")
accountMenu = menuBar.addMenu("&Scratch")
helpMenu = menuBar.addMenu("&Help")
toolsMenu.addAction("&Download JSON")
toolsMenu.addAction("&Preferences")
toolsMenu.addAction("View page on &Scratch")
helpMenu.addAction("&Basic help")
helpMenu.addAction("Advanced &topics")
helpMenu.addAction("&About Scratch2Python")
accountMenu.addAction("&Log in")  # swap with to sign out if logged in
accountMenu.addAction("Your &profile")
window.setWindowTitle("Scratch Homepage - Scratch2Python")



# TODO
# Add sources list
# Add filters
layout.setContentsMargins(0, 0, 0, 0)

app.setStyleSheet(
    """

    QMainWindow {
        background: #ffffff;
    }
    * {
        font-family: "Roboto", "Segoe UI", "San Francisco", "DejaVu Sans", "Verdana", "Arial", sans-serif;
        color: #212121;
    }
    QMenuBar::item {
        padding: 4px;
    }
    QMenuBar::item::selected {
        background-color: #26C6DA;
    }
    QMenuBar {
        background: #ffffff;
        border: none;
    }
    QMenu {
        padding: 4px;
        border: none;
        background: #ffffff;
    }
    QMenu::item {
        padding: 4px;
    }
    QMenu::item::selected {
        background-color: #26C6DA;
    }
    QPushButton {
        background-color: #26C6DA;
        border: none;
        border-radius: 0;
        padding: 8px;
        outline: none;
    }
    QPushButton::pressed {
        background: #0097A7;
        color: #ffffff;
    }
    """
)

if __name__ == "__main__":
    window.setLayout(layout)
    window.show()
    app.exec()
