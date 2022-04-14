import tkinter as tk
from tkinter import messagebox
import os, requests, threading
from utils import utils_function
from threadSignal.signal import Signal
from utils.message import Message
import time
import uuid
from models.tableItem import tableItem
from datetime import datetime


class fileDownload:
    def __init__(self):
        self.uid = -1

    # check if path and link are ok and start download
    def check_download_info(self, link, dir, scMW, sch):
        # initialize tk window
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()

        # Check if path selected exist
        if not os.path.exists(dir):
            # show message box if selected path not exist
            messagebox.showwarning(title="Error",
                                   message="The selected path doesn't exist. Please select a correct one.")
            return

        # Check if is a correct link
        if link.find('/') == -1 or link == '':
            # show message box if link is not an URL
            messagebox.showwarning(title="Error",
                                   message="This is not an URL. Please insert a correct one.")
            return

        filename = os.path.basename(link)
        extension = filename.split('.')[-1]

        # Check if file has an extension
        if len(extension) < 1:
            # show message box if link has not an extension
            messagebox.showwarning(title="Error",
                                   message="The link hasn't an extension.")
            return

        # check if filename is too long
        if len(filename) > 50:
            filename = filename[-50:]
            # show message box if filename is too long
            messagebox.showwarning(title="Warning",
                                   message="Filename too long. It will be formed by the last 50 characters")
            return

        # Check if file already exist in the folder
        if os.path.isfile(dir + '/' + filename):
            # show message box if file already exist in the folder
            messagebox.showwarning(title="Error",
                                   message="The file already exist in the folder.")
            return

        # start event threads
        event_thread_pause = threading.Event()
        event_thread_pause.clear()
        event_thread_interrupt = threading.Event()
        event_thread_interrupt.clear()
        event_thread_remove = threading.Event()
        event_thread_remove.clear()

        # initialize and start download thread daemon
        download_thread = threading.Thread(target=lambda: self.downloadItem(link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, event_thread_remove, sch))
        download_thread.setDaemon(True)
        download_thread.start()


    # start a new download
    def downloadItem(self, link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, event_thread_remove, sch):
        # request http for download
        resume_header = {'Range': 'bytes=%d-' % 0}
        r = requests.get(link, headers=resume_header, stream=True,  verify=False, allow_redirects=True)

        # open file download
        file = open(dir + '/' + filename, "wb")

        # r.headers contains info relative to download
        total_bytes = int(r.headers['content-length'])
        percentage = 0
        speed = 0

        # compute dimension of download
        file_dimension = utils_function.convert_size(total_bytes)

        uid = uuid.uuid4().fields[-1] # unique id thread
        self.uid = uid

        # current datetime
        now = datetime.now()
        dt_string_start = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        # creating tableItem object (started download)
        tableitem_id = uuid.uuid4().fields[-1] # id univoco tableitem
        ti = tableItem(self.uid, tableitem_id, filename, 'Started', file_dimension, dt_string_start, "N/A")
        # message to be send to history controller with signal
        messageHistory = Message([ti])
        signalHistory = Signal(messageHistory)
        signalHistory.messageChanged.connect(sch.addTableItem)
        signalHistory.start()
        signalHistory.disconnect()

        # message to be send to MainWindow controller with signal
        message = Message([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, 0, total_bytes])
        signal = Signal(message)
        signal.messageChanged.connect(scMW.addDownload)
        signal.start()
        signal.disconnect()

        # bytes downloaded
        dl_total = 0 # bytes of file downloaded overall
        dl_partial = 0 # bytes of file download from restart
        # signal connected to MainWindow controller function that update the download values
        signal.messageChanged.connect(scMW.updateDownloadItemValues)
        start = time.time()
        paused = False

        # download started
        for chunk in r.iter_content(chunk_size=256*1024):
            # download divided in chunk
            if chunk:
                # signal connected to MainWindow controller function that update the download values
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
                    # update values of tableItem
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return

                if event_thread_pause.isSet() is False:
                    # download continue normally
                    # update bytes downloaded and write the chunk on file
                    dl_total += len(chunk)
                    dl_partial += len(chunk)
                    file.write(chunk)
                    # calculate average speed
                    speed = round(((dl_partial // (time.time() - start)) / 100000) / 8, 5)

                else:
                    # download remain in pause
                    paused = True
                    speed = -1
                    percentage = round(dl_total * 100. / int(total_bytes), 1)
                    # if downloaded interrupted we update the views
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    # update values of tableItem
                    ti.updateValues(filename, 'Paused', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    file.close()
                    break

                # calculate percentage of download and update the MainWindow view
                percentage = round(dl_total * 100. / int(total_bytes), 1)
                message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                signal.emitSignal()

        if not paused:
            # download complete and we update the views
            now = datetime.now()
            dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
            ti.updateValues(filename, 'Completed', file_dimension, dt_string_start, dt_string_end)
            signalHistory.messageChanged.connect(sch.updateTableItem)
            messageHistory.changeData([ti])
            signalHistory.emitSignal()
            message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
            signal.emitSignal()
            file.close()
            messageHistory = None
            signalHistory = None
            network = None
            signal = None
        else:
            # download paused, waiting for a user choice
            while event_thread_pause.isSet() is True:
                start = time.time()
                dl_partial = 0
                speed = -1
                percentage = round(dl_total * 100. / int(total_bytes), 1)
                if event_thread_remove.isSet() is True:
                    # if download removed we close the file and remove the file from folder
                    os.remove(dir + '/' + filename)
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return
                if event_thread_interrupt.isSet() is False and event_thread_remove.isSet() is False:
                    # download not interrupted and remove (so remain in pause)
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                elif event_thread_interrupt.isSet() is True and event_thread_remove.isSet() is False:
                    # if downloaded interrupted we update the views
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    # update values of tableItem
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    file.close()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return
                time.sleep(0.2) # a little sleep


    # start an interrupted download
    def restartDownload(self, link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, uid, event_thread_remove, sch):
        # request http for download
        resume_header = {'Range': 'bytes=%d-' % 0}
        r = requests.get(link, headers=resume_header, stream=True,  verify=False, allow_redirects=True)

        # open file download (in this case we use append mode)
        file = open(dir + '/' + filename, "ab")

        # r.headers contains info relative to download
        total_bytes = int(r.headers['content-length'])
        percentage = 0
        speed = 0

        # compute dimension of download
        file_dimension = utils_function.convert_size(total_bytes)

        self.uid = uid # unique id

        # current datetime
        now = datetime.now()
        dt_string_start = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
        tableitem_id = uuid.uuid4().fields[-1] # id univoco tableItem
        # creating tableItem object (restarted download)
        ti = tableItem(self.uid, tableitem_id, filename, 'Restarted', file_dimension, dt_string_start, "N/A")
        # message to be send to history controller with signal
        messageHistory = Message([ti])
        signalHistory = Signal(messageHistory)
        signalHistory.messageChanged.connect(sch.addTableItem)
        signalHistory.start()
        signalHistory.disconnect()

        # message to be send to MainWindow controller with signal
        message = Message([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, 0, total_bytes])
        signal = Signal(message)
        signal.messageChanged.connect(scMW.updateDownloadItemValues)
        signal.start()
        signal.disconnect()

        # bytes downloaded
        dl_total = 0 # bytes of file downloaded overall
        dl_partial = 0 # bytes of file download from restart
        start = time.time()
        paused = False

        # download started
        for chunk in r.iter_content(chunk_size=256*1024):
            # download divided in chunk
            if chunk:
                # signal connected to MainWindow controller function that update the download values
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
                    # update values of tableItem
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return

                if event_thread_pause.isSet() is False:
                    # download continue normally
                    # update bytes downloaded and write the chunk on file
                    dl_total += len(chunk)
                    dl_partial += len(chunk)
                    file.write(chunk)
                    # calculate average speed
                    speed = round(((dl_partial // (time.time() - start)) / 100000) / 8, 5)

                else:
                    # download remain in pause
                    paused = True
                    speed = -1
                    percentage = round(dl_total * 100. / int(total_bytes), 1)
                    # if downloaded interrupted we update the views
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    # update values of tableItem
                    ti.updateValues(filename, 'Paused', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    file.close()
                    break

                # calculate percentage of download and update the MainWindow view
                percentage = round(dl_total * 100. / int(total_bytes), 1)
                message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                signal.emitSignal()

        if not paused:
            # download complete and we update the views
            now = datetime.now()
            dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
            ti.updateValues(filename, 'Completed', file_dimension, dt_string_start, dt_string_end)
            signalHistory.messageChanged.connect(sch.updateTableItem)
            messageHistory.changeData([ti])
            signalHistory.emitSignal()
            message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
            signal.emitSignal()
            file.close()
            messageHistory = None
            signalHistory = None
            network = None
            signal = None
        else:
            # download paused, waiting for a user choice
            while event_thread_pause.isSet() is True:
                start = time.time()
                dl_partial = 0
                speed = -1
                percentage = round(dl_total * 100. / int(total_bytes), 1)
                if event_thread_remove.isSet() is True:
                    # if download removed we close the file and remove the file from folder
                    os.remove(dir + '/' + filename)
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return
                if event_thread_interrupt.isSet() is False and event_thread_remove.isSet() is False:
                    # download not interrupted and remove (so remain in pause)
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                elif event_thread_interrupt.isSet() is True and event_thread_remove.isSet() is False:
                    # if downloaded interrupted we update the views
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    # update values of tableItem
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    file.close()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return
                time.sleep(0.2) # a little sleep


    # For future implementation (download resume)
    def resumeDownload(self, link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, uid, event_thread_remove, sch, bytes_read, total_bytes):
        resume_header = {'Range': 'bytes=%d-' % bytes_read}
        r = requests.get(link, headers=resume_header, stream=True,  verify=False, allow_redirects=True)
        # r = requests.get(link, stream=True)
        file = open(dir + '/' + filename, "ab")

        # r.headers contains info relative to download
        file_dimension_remain_original = int(r.headers['content-length'])
        percentage = round(bytes_read * 100. / int(total_bytes), 1)
        speed = 0

        # compute dimension
        file_dimension_remain = utils_function.convert_size(file_dimension_remain_original)
        file_dimension = utils_function.convert_size(total_bytes)

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
        message = Message([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, bytes_read, total_bytes])
        signal = Signal(message)
        signal.messageChanged.connect(scMW.updateDownloadItemValues)
        signal.start()
        signal.disconnect()

        dl_total = bytes_read
        dl_partial = 0
        start = time.time()
        paused = False

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
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
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

                else:
                    # download remain in pause
                    paused = True
                    speed = -1
                    percentage = round(dl_total * 100. / int(total_bytes), 1)
                    # if downloaded interrupted we update the views
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    # update values of tableItem
                    ti.updateValues(filename, 'Paused', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    file.close()
                    break

                percentage = round(dl_total * 100. / int(total_bytes), 1)
                message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                signal.emitSignal()

        if not paused:
            # download complete and we update the views
            now = datetime.now()
            dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
            ti.updateValues(filename, 'Completed', file_dimension, dt_string_start, dt_string_end)
            signalHistory.messageChanged.connect(sch.updateTableItem)
            messageHistory.changeData([ti])
            signalHistory.emitSignal()
            message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, 100, 'Completed', file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
            signal.emitSignal()
            file.close()
            messageHistory = None
            signalHistory = None
            network = None
            signal = None
        else:
            # download paused, waiting for a user choice
            while event_thread_pause.isSet() is True:
                start = time.time()
                dl_partial = 0
                speed = -1
                percentage = round(dl_total * 100. / int(total_bytes), 1)
                if event_thread_remove.isSet() is True:
                    # if download removed we close the file and remove the file from folder
                    os.remove(dir + '/' + filename)
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return
                if event_thread_interrupt.isSet() is False and event_thread_remove.isSet() is False:
                    # download not interrupted and remove (so remain in pause)
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                elif event_thread_interrupt.isSet() is True and event_thread_remove.isSet() is False:
                    # if downloaded interrupted we update the views
                    now = datetime.now()
                    dt_string_end = now.strftime("%d/%m/%Y %H:%M:%S") # dd/mm/YY H:M:S
                    # update values of tableItem
                    ti.updateValues(filename, 'Interrupted', file_dimension, dt_string_start, dt_string_end)
                    # update values of tableItem with signal send to history controller
                    signalHistory.messageChanged.connect(sch.updateTableItem)
                    messageHistory.changeData([ti])
                    signalHistory.emitSignal()
                    # update values of parameters with signal send to MainWindow controller
                    message.changeData([link, dir, filename, scMW, event_thread_pause, event_thread_interrupt, percentage, speed, file_dimension, uid, self, event_thread_remove, sch, ti, dl_total, total_bytes])
                    signal.emitSignal()
                    file.close()
                    messageHistory = None
                    signalHistory = None
                    network = None
                    signal = None
                    return
                time.sleep(0.2) # a little sleep