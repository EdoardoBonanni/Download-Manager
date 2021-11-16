from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import threading
from download import Download

class downloadItemController(QWidget):
    def __init__(self, downloadItemView, link, dir, filename, sc, event_thread_pause, event_thread_interrupt, uid, download_object):
        super(QWidget, self).__init__()
        self.ui = downloadItemView
        self.link = link
        self.dir = dir
        self.filename = filename
        self.sc = sc
        self.event_thread_pause = event_thread_pause
        self.event_thread_interrupt = event_thread_interrupt
        self.uid = uid
        self.download_object = download_object

        self.actions()

    def actions(self):
        self.ui.button_pause.clicked.connect(self.pause)
        self.ui.button_resume.clicked.connect(self.resume)
        self.ui.button_interrupt.clicked.connect(self.interrupt)
        self.ui.button_remove.clicked.connect(self.remove)

    def pause(self):
        if self.event_thread_interrupt.isSet() is False:
            print('pause')
            self.event_thread_pause.clear()

    def resume(self):
        if self.event_thread_interrupt.isSet() is False:
            print('resume after pause')
            self.event_thread_pause.set()
        else:
            print('resume after interrupt')
            self.event_thread_pause.set()
            self.event_thread_interrupt.clear()
            download_thread = threading.Thread(target=lambda: self.download_object.restartDownload(self.link, self.dir, self.filename, self.sc, self.event_thread_pause, self.event_thread_interrupt, self.uid))
            download_thread.start()

    def interrupt(self):
        if self.ui.label_speed.text() != 'Completed':
            print('interrupt')
            self.event_thread_interrupt.set()

    def remove(self):
        print('remove')






