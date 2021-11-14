import sys
from PyQt5 import QtWidgets
from controller import Controller
from MainWindow import Ui_mainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # mainWindow = QtWidgets.QMainWindow()
    # ui = Ui_mainWindow()
    # ui.setupUi(ui)
    # mainWindow.show()
    controller = Controller()
    controller.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
