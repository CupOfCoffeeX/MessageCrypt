import sys
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMessageBox, QTabWidget


from MainGUI import Ui_MainWindow

class Window(QMainWindow):
    """fenêtre principale"""
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Chat-Client")

        """self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)"""

        self.runSecondMainWindow()

        self.show()

        print('okokok')

    def closeEvent(self, event):
        """lorsqu'on clique sur la croix rouge on affiche cette fenêtre"""
        close = QMessageBox()
        close.setText("Voullez-vous vraiment quitter ?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def runSecondMainWindow(self):
        self.secondMainWindow = Ui_MainWindow(self)
        self.secondMainWindow.setupUi(self)






def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()