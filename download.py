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

        event_thread = threading.Event()
        event_thread.set()
        download_thread = threading.Thread(target=lambda: self.downloadItem(link, dir, filename, event_thread, sc))
        download_thread.start()

    def downloadItem(self, link, dir, filename, event_thread, sc):
        r = requests.get(link, stream=True)
        # file = open(dir + '/' + filename, "wb")

        # r.headers contains info relative to download
        file_dimension_original = int(r.headers['content-length'])
        download_percentage = 0
        speed = 0

        # compute dimension
        file_dimension = utils.convert_size(file_dimension_original)

        uid = uuid.uuid4().fields[-1] # id univoco
        self.uid = uid

        network = Message([filename, download_percentage, speed, file_dimension, uid])
        signal = Signal(network)
        signal.messageChanged.connect(sc.addDownload)
        signal.start()
        signal.disconnect()

        signal.messageChanged.connect(sc.updateDownloadValues)
        dl = 0
        start = time.time()
        for chunk in r.iter_content(chunk_size=256*1024):
            if chunk:
                # time.sleep(0.05) # a little sleep so you can see the bar progress
                dl += len(chunk)
                # file.write(chunk)
                speed = round(((dl // (time.time() - start)) / 100000) / 8, 5)
                percentage = round(dl * 100. / int(file_dimension_original), 1)

                network.changeData([filename, percentage, speed, file_dimension, uid])
                signal.emitSignal()

        network.changeData([filename, 100, 'Completed', file_dimension, uid])
        signal.emitSignal()
        # file.close()
        print('Download Completed')


