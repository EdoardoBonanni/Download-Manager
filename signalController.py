from PyQt5 import QtCore, QtGui, QtWidgets
from downloadItemView import downloadItemView
from MainWindow import Ui_mainWindow
from downloadItemController import downloadItemController


class signalController(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.ui = mainWindow
        self.downloadItems = []
        self.downloadItemsControllers = []

    @QtCore.pyqtSlot(list)
    def addDownload(self, list):
        # print("Adding a download widget")
        # list contains link, dir, filename, sc, event_thread_pause, event_thread_interrupt, download_percentage, speed, file_dimension, uid, download object (of the class), event_thread_remove
        d = downloadItemView(list[2], list[6], list[7], list[8]) # we need file_name, download_percentage, speed, dimension
        dic = downloadItemController(d, list[0], list[1], list[2],
                                     list[3], list[4], list[5], list[9], list[10], list[11]) # we need downloadItemView, all values of list (except download_percentage, speed, file_dimension)
        self.downloadItems.append((d, list[9])) # append to downloadItems a tuple with downloadItemView and uid
        self.downloadItemsControllers.append(dic)
        self.ui.scrollAreaWidgetLayout.removeItem(self.ui.spacerVertical_downloadList)
        self.ui.scrollAreaWidgetLayout.addWidget(d)
        self.ui.scrollAreaWidgetLayout.addItem(self.ui.spacerVertical_downloadList)

    @QtCore.pyqtSlot(list)
    def updateDownloadItemValues(self, list):
        # print("Update downloadItem values")
        # print(list)
        tupla = [item[0] for item in self.downloadItems if item[1] == list[9]] # search downloadItem with a specific uid in list of tuples
        d = tupla[0] # get downloadItemView
        # d.label_download_percentage.setText(str(list[1]) + '%')
        d.progressBar.setProperty("value", int(list[6])) # set value of progressbar with download_percentage
        if isinstance(list[7], str): #check type of speed variable
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
    def updateDownloadItemValues(self, list):
        # list contains downloadItemView, signalController, uid
        self.downloadItems.remove((list[0], list[2])) # we need downloadItemView, uid
        self.downloadItemsControllers.remove(list[1]) # we need signalController
        self.ui.scrollAreaWidgetLayout.removeWidget(list[0]) # we need downloadItemView
        print('eliminate')



