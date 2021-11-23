from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import threading
from download import Download
from message import Message
from signal import Signal
import os

class downloadItemController(QWidget):
    def __init__(self, downloadItemView, link, dir, filename, sc, event_thread_pause, event_thread_interrupt, uid, download_object, event_thread_remove):
        super(QWidget, self).__init__()
        self.downloadItemView = downloadItemView
        self.link = link
        self.dir = dir
        self.filename = filename
        self.sc = sc
        self.event_thread_pause = event_thread_pause
        self.event_thread_interrupt = event_thread_interrupt
        self.uid = uid
        self.download_object = download_object
        self.event_thread_remove = event_thread_remove

        self.actions()

    def actions(self):
        self.downloadItemView.button_pause.clicked.connect(self.pause)
        self.downloadItemView.button_resume.clicked.connect(self.resume)
        self.downloadItemView.button_interrupt.clicked.connect(self.interrupt)
        self.downloadItemView.button_remove.clicked.connect(self.remove)

    def pause(self):
        if self.event_thread_interrupt.isSet() is False:
            # print('pause')
            self.event_thread_pause.set()

    def resume(self):
        if self.event_thread_interrupt.isSet() is False:
            # print('resume after pause')
            self.event_thread_pause.clear()
        else:
            # print('resume after interrupt')
            self.event_thread_pause.clear()
            self.event_thread_interrupt.clear()
            download_thread = threading.Thread(target=lambda: self.download_object.restartDownload(self.link, self.dir, self.filename, self.sc, self.event_thread_pause, self.event_thread_interrupt, self.uid, self.event_thread_remove))
            download_thread.start()

    def interrupt(self):
        if self.downloadItemView.label_speed.text() != 'Completed':
            # print('interrupt')
            self.event_thread_interrupt.set()

    def remove(self):
        if self.event_thread_remove.isSet() is False:
            self.event_thread_remove.set()
            message = Message([self.downloadItemView, self, self.uid])
            signal = Signal(message)
            signal.messageChanged.connect(self.sc.remove)
            signal.start()
            if self.event_thread_interrupt.isSet() is True:
                os.remove(self.dir + '/' + self.filename)
            signal = None






