import sys
from PyQt5 import QtWidgets
from controller import Controller
from model import Model

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    # mainWindow = QtWidgets.QMainWindow()
    # ui = MainWindow.Ui_mainWindow()
    # ui.setupUi(mainWindow)
    # mainWindow.show()
    model = Model()
    controller = Controller(model)
    controller.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
