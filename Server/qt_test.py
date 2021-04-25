import sys
import socket
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QMessageBox


from Main import Ui_MainWindow

class Window(QMainWindow):
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