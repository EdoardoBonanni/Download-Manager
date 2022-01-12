from PyQt5.QtWidgets import QWidget
import threading
from utils.message import Message
from threadSignal.signal import Signal
import os
from datetime import datetime

class downloadItemController(QWidget):
    def __init__(self, downloadItemView, link, dir, filename, signalControllerMW, event_thread_pause, event_thread_interrupt, uid, fileDownload_object, event_thread_remove, signalControllerHistory, tableItem, bytes_read, total_bytes):
        super(QWidget, self).__init__()
        self.downloadItemView = downloadItemView
        self.link = link
        self.dir = dir
        self.filename = filename
        self.scMW = signalControllerMW
        self.event_thread_pause = event_thread_pause
        self.event_thread_interrupt = event_thread_interrupt
        self.uid = uid
        self.fileDownload_object = fileDownload_object
        self.event_thread_remove = event_thread_remove
        self.sch = signalControllerHistory
        self.ti = tableItem
        self.bytes_read = bytes_read
        self.total_bytes = total_bytes

        self.actions()


    def actions(self):
        self.downloadItemView.button_pause.clicked.connect(self.pause)
        self.downloadItemView.button_resume.clicked.connect(self.resume)
        self.downloadItemView.button_interrupt.clicked.connect(self.interrupt)
        self.downloadItemView.button_remove.clicked.connect(self.remove)


    def updateBytesRead(self, bytes_read):
        self.bytes_read = bytes_read


    def pause(self):
        if self.event_thread_interrupt.isSet() is False:
            self.event_thread_pause.set()


    def interrupt(self):
        if self.downloadItemView.label_speed.text() != 'Completed':
            self.event_thread_interrupt.set()


    def remove(self):
        if self.event_thread_remove.isSet() is False:
            self.event_thread_remove.set()
            # we need to remove a download from scrollAreaWidgetLayout sending a signal to scMW
            # the message contains downloadItemView, downloadItemController (itself) and uid of download
            message = Message([self.downloadItemView, self, self.uid])
            signal = Signal(message)
            signal.messageChanged.connect(self.scMW.remove)
            signal.start()

            now = datetime.now()
            dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
            values = self.ti.getValues()

            # Furthermore we send a signal to signalControllerHistory (sch) if download is not completed
            if values[6] == 'N/A': # check if download is already completed
                self.ti.updateValues(values[2], 'Interrupted', values[4], values[5], dt_string_end) # filename, status, dimension, time_start, time_end
                messageHistory = Message([self.ti])
                signalHistory = Signal(messageHistory)
                signalHistory.messageChanged.connect(self.sch.updateTableItem)
                signalHistory.start()

            # we remove the partial file drom the folder
            if self.event_thread_interrupt.isSet() is True:
                os.remove(self.dir + '/' + self.filename)

            messageHistory = None
            signalHistory = None
            message = None
            signal = None






