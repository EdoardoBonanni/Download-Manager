from PyQt5 import QtCore, QtGui, QtWidgets
import threading

class Signal(QtCore.QObject):
    messageChanged = QtCore.pyqtSignal(list)

    def __init__(self, network, parent=None):
        super().__init__(parent)
        self.network = network

    def start(self):
        threading.Thread(target=self._execute, daemon=True).start()

    def _execute(self):
        try:
            message = self.network.receiveData()
            if message:
                self.messageChanged.emit(message)
        except:
            print("Disconnected.")

