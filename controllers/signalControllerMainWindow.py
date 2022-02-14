from PyQt5 import QtCore, QtWidgets
from views.downloadItemView import downloadItemView
from views.MainWindow import Ui_mainWindow
from controllers.downloadItemController import downloadItemController
import sip


class signalControllerMainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.ui = mainWindow
        self.downloadItems = [] # a list of download started, paused, interrupted or completed
        self.downloadItemsControllers = [] # a list of controllers of previous downloads


    @QtCore.pyqtSlot(list)
    def addDownload(self, list):
        # list contains link, dir, filename, scMW (itself), event_thread_pause, event_thread_interrupt, download_percentage, speed, file_dimension, uid, fileDownload (object), event_thread_remove, sch (signalControllerHistory), tableItem (object), bytes_read, total_bytes
        link = list[0]
        dir = list[1]
        filename = list[2]
        scMW = list[3]
        event_thread_pause = list[4]
        event_thread_interrupt = list[5]
        download_percentage = list[6]
        speed = list[7]
        file_dimension = list[8]
        uid = list[9]
        fileDownload = list[10]
        event_thread_remove = list[11]
        sch = list[12]
        tableItem = list[13]
        bytes_read = list[14]
        total_bytes = list[15]
        d = downloadItemView(filename, download_percentage, speed, file_dimension)
        dic = downloadItemController(d, link, dir, filename,
                                     scMW, event_thread_pause, event_thread_interrupt, uid, fileDownload, event_thread_remove,
                                     sch, tableItem, bytes_read, total_bytes)
        # we need downloadItemView, link, dir, filename, scMW (itself), event_thread_pause, event_thread_interrupt,  uid,
        # fileDownload (object), event_thread_remove, sch (signalControllerHistory), tableItem (object), bytes_read, total_bytes

        self.downloadItems.append((d, uid)) # append to downloadItems a tuple with downloadItemView and uid
        self.downloadItemsControllers.append(dic) # add a controller of this download to downloadItemsControllers list
        self.ui.scrollAreaWidgetLayout.removeItem(self.ui.spacerVertical_downloadList)
        self.ui.scrollAreaWidgetLayout.addWidget(d) # add downloadItemView to scrollAreaWidgetLayout
        self.ui.scrollAreaWidgetLayout.addItem(self.ui.spacerVertical_downloadList)


    @QtCore.pyqtSlot(list)
    def updateDownloadItemValues(self, list):
        # list contains link, dir, filename, scMW (itself), event_thread_pause, event_thread_interrupt, download_percentage, speed, file_dimension, uid, fileDownload (object), event_thread_remove, sch (signalControllerHistory), tableItem (object), bytes_read, total_bytes
        event_thread_interrupt = list[5]
        download_percentage = list[6]
        speed = list[7]
        uid = list[9]
        bytes_read = list[14]
        idx = [idx for idx, item in enumerate(self.downloadItems) if item[1] == uid] # search index of downloadItem with a specific uid in list of tuples
        idx = idx[0]
        d = self.downloadItems[idx][0] # get downloadItemView
        dic = self.downloadItemsControllers[idx] # get downloadItemController
        dic.updateBytesRead(bytes_read) # update bytes_read
        d.progressBar.setProperty("value", int(download_percentage)) # set value of progressbar with download_percentage
        if isinstance(speed, str): # check type of speed variable
            d.label_speed.setText(speed) # download completed insert in speed label
            d.button_pause.hide()
            d.button_resume.hide()
            d.button_interrupt.hide()
        else:
            if event_thread_interrupt.isSet() is True: # check if thread is interrupted
                d.button_pause.hide()
                d.button_resume.show()
                d.button_interrupt.hide()
                d.label_speed.setText('Interrupted') # Interrupted
            else:
                d.button_pause.show()
                d.button_resume.show()
                d.button_interrupt.show()
                if 0 <= speed < 1: # check download speed
                    speedKb = str(round(speed * 1000, 1)) + ' KB/s'
                    d.label_speed.setText(speedKb) # download speed KB/s
                elif list[7] >= 1:
                    speedMb = str(round(speed, 1)) + ' MB/s'
                    d.label_speed.setText(speedMb) # download speed MB/s
                else:
                    d.label_speed.setText('Paused') # Paused
                    d.button_pause.hide()


    @QtCore.pyqtSlot(list)
    def remove(self, list):
        # list contains downloadItemView, downloadItemController, uid
        downloadItemView = list[0]
        downloadItemController = list[1]
        uid = list[2]
        self.downloadItems.remove((downloadItemView, uid)) # we remove downloadItemView from downloadItems list
        self.downloadItemsControllers.remove(downloadItemController) # we remove the respective controller from downloadItemsControllers list
        self.ui.scrollAreaWidgetLayout.removeWidget(downloadItemView) # we remove the downloadItemView from the scrollAreaWidgetLayout
        sip.delete(downloadItemView) # we invoke the destructor. it's necessary to avoid problem with child of downloadItemView
        list[0] = None
