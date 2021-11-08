import MainWindow
import sys
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow.Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
