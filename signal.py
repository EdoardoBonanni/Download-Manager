from PyQt5 import QtCore, QtGui, QtWidgets
import threading

class Signal(QtCore.QObject):
    messageChanged = QtCore.pyqtSignal(list)

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message

    def start(self):
        threading.Thread(target=self._execute, daemon=True).start()

    def emitSignal(self):
        self._execute()

    # execution of thread with private method
    def _execute(self):
        try:
            message = self.message.receiveData()
            if message:
                self.messageChanged.emit(message)
        except:
            print("Disconnected.")

