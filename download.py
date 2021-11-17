import tkinter as tk
from tkinter import messagebox
import os, requests, threading, utils
from signal import Signal
from message import Message
import time
import uuid


class Download:
    def __init__(self):
        self.uid = -1

    def check_download_info(self, link, dir, sc):
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()

        # Check if path selected exist
        if not os.path.exists(dir):
            messagebox.showwarning(title="Error",
                                   message="The selected path doesn't exist. Please select a correct one.")
            return

        # Check if is a correct link
        if link.find('/') == -1 or link == '':
            messagebox.showwarning(title="Error",
                                   message="This is not an URL. Please insert a correct one.")
            return

        filename = os.path.basename(link)
        extension = filename.split('.')[-1]

        # Check if file has an extension
        if len(extension) < 1:
            messagebox.showwarning(title="Error",
                                   message="The link hasn't an extension.")
            return

        # Check if file already exist in the folder
        if os.path.isfile(dir + '/' + filename):
            messagebox.showwarning(title="Error",
                                   message="The file already exist in the folder.")
            return

        event_thread_pause = threading.Event()
        event_thread_pause.set()
        event_thread_interrupt = threading.Event()
        event_thread_interrupt.clear()
        download_thread = threading.Thread(target=lambda: self.downloadItem(link, dir, filename, sc, event_thread_pause, event_thread_interrupt))
        download_thread.start()

    def downloadItem(self, link, dir, filename, sc, event_thread_pause, event_thread_interrupt):
        r = requests.get(link, stream=True)
        # file = open(dir + '/' + filename, "wb")

        # r.headers contains info relative to download
        file_dimension_original = int(r.headers['content-length'])
        percentage = 0
        speed = 0

        # compute dimension
        file_dimension = utils.convert_size(file_dimension_original)

        uid = uuid.uuid4().fields[-1] # id univoco
        self.uid = uid

        network = Message([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
        signal = Signal(network)
        signal.messageChanged.connect(sc.addDownload)
        signal.start()
        signal.disconnect()

        dl_total = 0
        dl_partial = 0
        signal.messageChanged.connect(sc.updateDownloadItemValues)
        start = time.time()
        for chunk in r.iter_content(chunk_size=256*1024):
            if chunk:
                signal.messageChanged.connect(sc.updateDownloadItemValues)
                if event_thread_interrupt.isSet() is True:
                    # file.close()
                    network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
                    signal.emitSignal()
                    network = None
                    signal = None
                    return

                if event_thread_pause.isSet() is True:
                    dl_total += len(chunk)
                    dl_partial += len(chunk)
                    # file.write(chunk)
                    speed = round(((dl_partial // (time.time() - start)) / 100000) / 8, 5)

                while event_thread_pause.isSet() is False:
                    start = time.time()
                    dl_partial = 0
                    speed = -1
                    percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                    network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
                    signal.emitSignal()

                    time.sleep(0.2) # a little sleep

                percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
                signal.emitSignal()

        network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self])
        signal.emitSignal()
        # file.close()
        print('Download Completed')


    def restartDownload(self, link, dir, filename, sc, event_thread_pause, event_thread_interrupt, uid):
        r = requests.get(link, stream=True)
        # file = open(dir + '/' + filename, "ab")

        # r.headers contains info relative to download
        file_dimension_original = int(r.headers['content-length'])
        percentage = 0
        speed = 0

        # compute dimension
        file_dimension = utils.convert_size(file_dimension_original)

        self.uid = uid

        network = Message([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
        signal = Signal(network)
        signal.messageChanged.connect(sc.updateDownloadItemValues)
        signal.start()
        signal.disconnect()

        dl_total = 0
        dl_partial = 0
        start = time.time()
        for chunk in r.iter_content(chunk_size=256*1024):
            if chunk:
                signal.messageChanged.connect(sc.updateDownloadItemValues)
                if event_thread_interrupt.isSet() is True:
                    # file.close()
                    network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
                    signal.emitSignal()
                    network = None
                    signal = None
                    return

                if event_thread_pause.isSet() is True:
                    dl_total += len(chunk)
                    dl_partial += len(chunk)
                    # file.write(chunk)
                    speed = round(((dl_partial // (time.time() - start)) / 100000) / 8, 5)

                while event_thread_pause.isSet() is False:
                    start = time.time()
                    dl_partial = 0
                    speed = -1
                    percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                    network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
                    signal.emitSignal()

                    time.sleep(0.2) # a little sleep

                percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self])
                signal.emitSignal()

        network.changeData([link, dir, filename, sc, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self])
        signal.emitSignal()
        # file.close()
        print('Download Completed')


