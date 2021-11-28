import tkinter as tk
from tkinter import messagebox
import os, requests, threading
from utils import utils_function
from threadSignal.signal import Signal
from utils.message import Message
import time
import uuid
from utils.tableItem import tableItem
from datetime import datetime


class fileDownload:
    def __init__(self):
        self.uid = -1

    def check_download_info(self, link, dir, scMW, sch):
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

        if len(filename) > 50:
            filename = filename[-50:]
            messagebox.showwarning(title="Warning",
                                   message="Filename too long. It will be formed by the last 50 characters")

        # Check if file already exist in the folder
        if os.path.isfile(dir + '/' + filename):
            messagebox.showwarning(title="Error",
                                   message="The file already exist in the folder.")
            return

        event_thread_pause = threading.Event()
        event_thread_pause.clear()
        event_thread_interrupt = threading.Event()
        event_thread_interrupt.clear()
        event_thread_remove = threading.Event()
        event_thread_remove.clear()
        download_thread = threading.Thread(target=lambda: self.downloadItem(link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, event_thread_remove, sch))
        download_thread.setDaemon(True)
        download_thread.start()

    def downloadItem(self, link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, event_thread_remove, sch):
        r = requests.get(link, stream=True)
        file = open(dir + '/' + filename, "wb")

        # r.headers contains info relative to download
        file_dimension_original = int(r.headers['content-length'])
        percentage = 0
        speed = 0

        # compute dimension
        file_dimension = utils_function.convert_size(file_dimension_original)

        uid = uuid.uuid4().fields[-1] # id univoco thread
        self.uid = uid

        # signal to history table
        now = datetime.now()
        dt_string_start = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        tableitem_id = uuid.uuid4().fields[-1] # id univoco tableitem
        ti = tableItem(self.uid, tableitem_id, filename, 'Started', file_dimension, dt_string_start, "N/A")
        messageHistory = Message([ti])
        signalHistory = Signal(messageHistory)
        signalHistory.messageChanged.connect(sch.addTableItem)
        signalHistory.start()
        signalHistory.disconnect()

        # signal to mainwindow
        message = Message([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
        signal = Signal(message)
        signal.messageChanged.connect(scMW.addDownload)
        signal.start()
        signal.disconnect()

        dl_total = 0
        dl_partial = 0
        signal.messageChanged.connect(scMW.updateDownloadItemValues)
        start = time.time()

        # download started
        for chunk in r.iter_content(chunk_size=256*1024):
            if chunk:
                signal.messageChanged.connect(scMW.updateDownloadItemValues)

                if event_thread_remove.isSet() is True:
                    # if download removed we close the file and remove the file from folder
                    file.close()
                    os.remove(dir + '/' + filename)
                    network = None
                    signal = None
                    return

                if event_thread_interrupt.isSet() is True:
                    # if downloaded interrupted we update the views
                    file.close()
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                    signal.emitSignal()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return

                if event_thread_pause.isSet() is False:
                    # download continue normally
                    dl_total += len(chunk)
                    dl_partial += len(chunk)
                    file.write(chunk)
                    speed = round(((dl_partial // (time.time() - start)) / 100000) / 8, 5)

                while event_thread_pause.isSet() is True:
                    # download remain in pause
                    start = time.time()
                    dl_partial = 0
                    speed = -1
                    percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                    if event_thread_remove.isSet() is True:
                        file.close()
                        os.remove(dir + '/' + filename)
                        messageHistory = None
                        signalHistory = None
                        network = None
                        signal = None
                        return
                    if event_thread_interrupt.isSet() is False and event_thread_remove.isSet() is False:
                        message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                        signal.emitSignal()
                    elif event_thread_interrupt.isSet() is True and event_thread_remove.isSet() is False:
                        now = datetime.now()
                        dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                        ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                        signalHistory.messageChanged.connect(sch.updateTableItem)
                        messageHistory.changeData([ti])
                        signalHistory.emitSignal()
                        message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                        signal.emitSignal()
                        file.close()
                        messageHistory = None
                        signalHistory = None
                        network = None
                        signal = None
                        return

                    time.sleep(0.2) # a little sleep

                percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                signal.emitSignal()

        # download complete and we update the views
        now = datetime.now()
        dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        ti.updateValues(filename, 'Completed', file_dimension, dt_string_start, dt_string_end)
        signalHistory.messageChanged.connect(sch.updateTableItem)
        messageHistory.changeData([ti])
        signalHistory.emitSignal()
        message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self, event_thread_remove, sch, ti])
        signal.emitSignal()
        file.close()
        messageHistory = None
        signalHistory = None
        network = None
        signal = None


    def restartDownload(self, link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, uid, event_thread_remove, sch):
        r = requests.get(link, stream=True)
        file = open(dir + '/' + filename, "ab")

        # r.headers contains info relative to download
        file_dimension_original = int(r.headers['content-length'])
        percentage = 0
        speed = 0

        # compute dimension
        file_dimension = utils_function.convert_size(file_dimension_original)

        self.uid = uid

        # signal to history table
        now = datetime.now()
        dt_string_start = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        tableitem_id = uuid.uuid4().fields[-1] # id univoco tableItem
        ti = tableItem(self.uid, tableitem_id, filename, 'Restarted', file_dimension, dt_string_start, "N/A")
        messageHistory = Message([ti])
        signalHistory = Signal(messageHistory)
        signalHistory.messageChanged.connect(sch.addTableItem)
        signalHistory.start()
        signalHistory.disconnect()

        # signal to mainwindow
        message = Message([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
        signal = Signal(message)
        signal.messageChanged.connect(scMW.updateDownloadItemValues)
        signal.start()
        signal.disconnect()

        dl_total = 0
        dl_partial = 0
        start = time.time()

        # download started
        for chunk in r.iter_content(chunk_size=256*1024):
            if chunk:
                signal.messageChanged.connect(scMW.updateDownloadItemValues)

                if event_thread_remove.isSet() is True:
                    # if download removed we close the file and remove the file from folder
                    file.close()
                    os.remove(dir + '/' + filename)
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return

                if event_thread_interrupt.isSet() is True:
                    # if downloaded interrupted we update the views
                    file.close()
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                    signal.emitSignal()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return

                if event_thread_pause.isSet() is False:
                    # download continue normally
                    dl_total += len(chunk)
                    dl_partial += len(chunk)
                    file.write(chunk)
                    speed = round(((dl_partial // (time.time() - start)) / 100000) / 8, 5)

                while event_thread_pause.isSet() is True:
                    # download remain in pause
                    start = time.time()
                    dl_partial = 0
                    speed = -1
                    percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                    if event_thread_remove.isSet() is True:
                        file.close()
                        os.remove(dir + '/' + filename)
                        messageHistory = None
                        signalHistory = None
                        network = None
                        signal = None
                        return
                    if event_thread_interrupt.isSet() is False and event_thread_remove.isSet() is False:
                        message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                        signal.emitSignal()
                    elif event_thread_interrupt.isSet() is True and event_thread_remove.isSet() is False:
                        now = datetime.now()
                        dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                        ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                        signalHistory.messageChanged.connect(sch.updateTableItem)
                        messageHistory.changeData([ti])
                        signalHistory.emitSignal()
                        message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                        signal.emitSignal()
                        file.close()
                        messageHistory = None
                        signalHistory = None
                        network = None
                        signal = None
                        return
                    time.sleep(0.2) # a little sleep

                percentage = round(dl_total * 100. / int(file_dimension_original), 1)
                message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti])
                signal.emitSignal()

        # download complete and we update the views
        now = datetime.now()
        dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        ti.updateValues(filename, 'Completed', file_dimension, dt_string_start, dt_string_end)
        signalHistory.messageChanged.connect(sch.updateTableItem)
        messageHistory.changeData([ti])
        signalHistory.emitSignal()
        message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self, event_thread_remove, sch, ti])
        signal.emitSignal()
        file.close()
        messageHistory = None
        signalHistory = None
        network = None
        signal = None

