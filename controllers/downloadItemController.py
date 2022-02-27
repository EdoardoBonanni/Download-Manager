from PyQt5.QtWidgets import QWidget
import threading
from utils.message import Message
from threadSignal.signal import Signal
import os
from datetime import datetime
from models.model_downloadItem import Model_downloadItem

class downloadItemController(QWidget):
    # controller for downloadItem
    def __init__(self, downloadItemView, link, dir, filename, signalControllerMW, event_thread_pause, event_thread_interrupt, uid, fileDownload_object, event_thread_remove, signalControllerHistory, tableItem, bytes_read, total_bytes):
        super(QWidget, self).__init__()

        # initialize the downloadItem model
        self.model = Model_downloadItem(downloadItemView, link, dir, filename, signalControllerMW, event_thread_pause, event_thread_interrupt, uid, fileDownload_object, event_thread_remove, signalControllerHistory, tableItem, bytes_read, total_bytes)

        # define the interactions
        self.interactions()

    def interactions(self):
        # events for pause, resume, interrupt and remove buttons
        self.model.downloadItemView.button_pause.clicked.connect(self.pause)
        self.model.downloadItemView.button_resume.clicked.connect(self.resume)
        self.model.downloadItemView.button_interrupt.clicked.connect(self.interrupt)
        self.model.downloadItemView.button_remove.clicked.connect(self.remove)

    def updateBytesRead(self, bytes_read):
        # update bytes download read
        self.model.bytes_read = bytes_read

    def pause(self):
        # check if download is interrupted
        if self.model.event_thread_interrupt.isSet() is False:
            # if the download is not interrupted, it resumes it after being paused
            self.model.event_thread_pause.set()

    def resume(self):
        # check if download is interrupted
        if self.model.event_thread_interrupt.isSet() is False:
            # if the download is not interrupted, it resumes
            self.model.event_thread_pause.clear()
        else:
            # else it starts again (restart)
            # reset the event threads
            self.model.event_thread_pause.clear()
            self.model.event_thread_interrupt.clear()
            # restart a download thread
            download_thread = threading.Thread(target=lambda: self.model.fileDownload_object.restartDownload(self.model.link, self.model.dir, self.model.filename, self.model.scMW, self.model.event_thread_pause, self.model.event_thread_interrupt, self.model.uid, self.model.event_thread_remove, self.model.sch))
            download_thread.setDaemon(True)
            download_thread.start()

    def interrupt(self):
        # check if download is not completed
        if self.model.downloadItemView.label_speed.text() != 'Completed':
            # if the download is not completed, it interrupt
            self.model.event_thread_interrupt.set()

    def remove(self):
        # check if download is not removed
        if self.model.event_thread_remove.isSet() is False:
            # set the event remove event thread
            self.model.event_thread_remove.set()
            # we need to remove a download from scrollAreaWidgetLayout sending a signal to scMW (signalControllerMainWindow)
            # the message contains downloadItemView, downloadItemController (itself) and uid of download
            message = Message([self.model.downloadItemView, self, self.model.uid])
            signal = Signal(message)
            signal.messageChanged.connect(self.model.scMW.remove)
            signal.start()

            # get the values of downloadItem
            now = datetime.now()
            dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
            values = self.model.ti.getValues()

            # Furthermore we send a signal to signalControllerHistory (sch) if download is not completed
            if values[6] == 'N/A': # check if download is already completed
                # update the values of downloadItem
                self.model.ti.updateValues(values[2], 'Interrupted', values[4], values[5], dt_string_end) # filename, status, dimension, time_start, time_end
                # update values of tableItem with signal send to history controller
                messageHistory = Message([self.model.ti])
                signalHistory = Signal(messageHistory)
                signalHistory.messageChanged.connect(self.model.sch.updateTableItem)
                signalHistory.start()

            # check if download is not interrupted
            if self.model.event_thread_interrupt.isSet() is True:
                # if the download is interrupted, we remove the partial file from the folder
                os.remove(self.model.dir + '/' + self.model.filename)

            messageHistory = None
            signalHistory = None
            message = None
            signal = None






