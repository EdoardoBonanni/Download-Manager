from PyQt5 import QtCore, QtGui, QtWidgets
import threading

class Signal(QtCore.QObject):
    # thread that contains a message to be sent to controllers to update views

    # signal that have to be emit when message is changed
    messageChanged = QtCore.pyqtSignal(list)

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message

    def start(self):
        # start the thread (daemon)
        threading.Thread(target=self._execute, daemon=True).start()

    def emitSignal(self):
        # emit signal
        self._execute()

    # execution of thread with private method
    def _execute(self):
        # update the message and send it to controllers
        try:
            message = self.message.receiveData()
            if message:
                self.messageChanged.emit(message)
        except:
            print("Disconnected.")

