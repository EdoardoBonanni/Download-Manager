import tkinter as tk
from tkinter import messagebox
import os, requests, threading, utils
from signal import Signal
from message import Message
import time

class Download:
    def __init__(self):
        self.name = ''

    def check_download_info(self, link, dir, ui):
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()

        # Check if path selected exist
        if not os.path.exists(dir):
            messagebox.showwarning(title="Error",
                                   message="The selected path doesn't exist. Please select a correct one")
            return

        if link.find('/') == -1:
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

        self.name = filename

        event_thread = threading.Event()
        event_thread.set()
        download_thread = threading.Thread(target=lambda: self.downloadItem(link, dir, filename, event_thread, ui))
        download_thread.start()

    def downloadItem(self, link, dir, filename, event_thread, ui):
        r = requests.get(link, stream=True)
        # file = open(dir + '/' + filename, "wb")

        # r.headers contains info relative to download
        file_dimension_original = int(r.headers['content-length'])
        download_percentage = 0
        speed = 0

        # compute dimension
        file_dimension = utils.convert_size(file_dimension_original)

        # network = Network('a')
        network = Message([filename, download_percentage, speed, file_dimension])
        signal = Signal(network)
        # signal.messageChanged.connect(ui.changeLabel)
        signal.messageChanged.connect(ui.addDownload)
        signal.start()
        signal.disconnect()

        signal.messageChanged.connect(ui.updateDownloadValues)
        dl = 0
        start = time.time()
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                # time.sleep(0.05) # a little sleep so you can see the bar progress
                dl += len(chunk)
                # file.write(chunk)
                speed = round((dl // (time.time() - start)) / 100000, 1)
                percentage = round(dl * 100. / int(file_dimension_original), 1)

                network.changeData([filename, percentage, speed, file_dimension])
                signal.start()

        network.changeData([filename, 100, 'Finished', file_dimension])
        signal.start()
        print('fine')


