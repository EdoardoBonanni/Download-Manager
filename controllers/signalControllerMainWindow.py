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

        d = downloadItemView(list[2], list[6], list[7], list[8]) # we need file_name, download_percentage, speed, dimension
        dic = downloadItemController(d, list[0], list[1], list[2],
                                     list[3], list[4], list[5], list[9], list[10], list[11], list[12], list[13], list[14], list[15])
        # we need downloadItemView, dir, filename, scMW (itself), event_thread_pause, event_thread_interrupt,  uid, fileDownload (object), event_thread_remove, sch (signalControllerHistory), tableItem (object), bytes_read, total_bytes

        self.downloadItems.append((d, list[9])) # append to downloadItems a tuple with downloadItemView and uid
        self.downloadItemsControllers.append(dic) # add a controller of this download to downloadItemsControllers list
        self.ui.scrollAreaWidgetLayout.removeItem(self.ui.spacerVertical_downloadList)
        self.ui.scrollAreaWidgetLayout.addWidget(d) # add downloadItemView to scrollAreaWidgetLayout
        self.ui.scrollAreaWidgetLayout.addItem(self.ui.spacerVertical_downloadList)


    @QtCore.pyqtSlot(list)
    def updateDownloadItemValues(self, list):
        idx = [idx for idx, item in enumerate(self.downloadItems) if item[1] == list[9]] # search index of downloadItem with a specific uid in list of tuples
        idx = idx[0]
        d = self.downloadItems[idx][0] # get downloadItemView
        dic = self.downloadItemsControllers[idx] # get downloadItemController
        bytes_read = list[14]
        dic.updateBytesRead(bytes_read) # update bytes_read
        d.progressBar.setProperty("value", int(list[6])) # set value of progressbar with download_percentage
        if isinstance(list[7], str): # check type of speed variable
            d.label_speed.setText(list[7]) # download completed insert in speed label
            d.button_pause.hide()
            d.button_resume.hide()
            d.button_interrupt.hide()
        else:
            if list[5].isSet() is True: # check if thread is interrupted
                d.button_pause.hide()
                d.button_resume.show()
                d.button_interrupt.hide()
                d.label_speed.setText('Interrupted') # Interrupted
            else:
                d.button_pause.show()
                d.button_resume.show()
                d.button_interrupt.show()
                if 0 <= list[7] < 1: # check download speed
                    speedKb = str(round(list[7] * 1000, 1)) + ' KB/s'
                    d.label_speed.setText(speedKb) # download speed KB/s
                elif list[7] >= 1:
                    speedMb = str(round(list[7], 1)) + ' MB/s'
                    d.label_speed.setText(speedMb) # download speed MB/s
                else:
                    d.label_speed.setText('Paused') # Paused
                    d.button_pause.hide()


    @QtCore.pyqtSlot(list)
    def remove(self, list):
        # list contains downloadItemView, downloadItemController, uid
        self.downloadItems.remove((list[0], list[2])) # we remove downloadItemView from downloadItems list
        self.downloadItemsControllers.remove(list[1]) # we remove the respective controller from downloadItemsControllers list
        self.ui.scrollAreaWidgetLayout.removeWidget(list[0]) # we remove the downloadItemView from the scrollAreaWidgetLayout
        sip.delete(list[0]) # we invoke the destructor. it's necessary to avoid problem with child of downloadItemView
        list[0] = None
