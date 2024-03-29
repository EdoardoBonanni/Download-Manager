import sys
from PyQt5 import QtWidgets
from controllers.controllerMainWindow import controllerMainWindow


def main():
    # initialize the application and start controllerMainWindow
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    controller = controllerMainWindow()
    controller.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
