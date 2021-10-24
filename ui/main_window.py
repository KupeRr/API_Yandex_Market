import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):

        self.setGeometry(300, 300, 600, 450)
        self.setWindowTitle('*SomeName*')

        self.label = QLabel('Welcome to helper *Name*!')
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {background-color: red;}")
        

        self.show()

    def init_welcome_window():
        pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())