from PyQt5 import QtCore, QtWidgets
from views.downloadItemView import downloadItemView
from views.MainWindow import Ui_mainWindow
from models.model_MainWindow import Model_MainWindow
from controllers.downloadItemController import downloadItemController
import sip

class signalControllerMainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    # controller that change the mainwindow receiving information from threads
    def __init__(self, mainWindow, model: Model_MainWindow, parent=None):
        super().__init__(parent)
        self.ui = mainWindow

        # model MainWindow
        self.model = model


    # add a new download to scrollArea
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

        # create downloadItemView object
        d = downloadItemView(filename, download_percentage, speed, file_dimension)

        # we need downloadItemView, link, dir, filename, scMW (itself), event_thread_pause, event_thread_interrupt,  uid, fileDownload (object), event_thread_remove, sch (signalControllerHistory), tableItem (object), bytes_read, total_bytes
        # to create downloadItemController object
        dic = downloadItemController(d, link, dir, filename,
                                     scMW, event_thread_pause, event_thread_interrupt, uid, fileDownload, event_thread_remove,
                                     sch, tableItem, bytes_read, total_bytes)

        # append to downloadItems a tuple with downloadItemView and uid
        self.model.downloadItems.append((d, uid))
        # add a controller of this download to downloadItemsControllers list
        self.model.downloadItemsControllers.append(dic)
        self.ui.scrollAreaWidgetLayout.removeItem(self.ui.spacerVertical_downloadList)
        # add downloadItemView to scrollAreaWidgetLayout
        self.ui.scrollAreaWidgetLayout.addWidget(d)
        self.ui.scrollAreaWidgetLayout.addItem(self.ui.spacerVertical_downloadList)


    # update values of a specific downloadItem
    @QtCore.pyqtSlot(list)
    def updateDownloadItemValues(self, list):
        # list contains link, dir, filename, scMW (itself), event_thread_pause, event_thread_interrupt, download_percentage, speed, file_dimension, uid, fileDownload (object), event_thread_remove, sch (signalControllerHistory), tableItem (object), bytes_read, total_bytes
        event_thread_interrupt = list[5]
        download_percentage = list[6]
        speed = list[7]
        uid = list[9]
        bytes_read = list[14]
        idx = [idx for idx, item in enumerate(self.model.downloadItems) if item[1] == uid] # search index of downloadItem with a specific uid in list of tuples
        if len(idx) > 0: 
            idx = idx[0]
            # get downloadItemView
            d = self.model.downloadItems[idx][0]
            # get downloadItemController
            dic = self.model.downloadItemsControllers[idx]
            # update bytes_read
            dic.updateBytesRead(bytes_read)
            # set value of progressbar with download_percentage
            d.progressBar.setProperty("value", int(download_percentage))
            # check type of speed variable
            if isinstance(speed, str):
                # speed have a str value so the download is completed
                # download completed insert in speed label
                d.label_speed.setText(speed)
                # hide buttons
                d.button_pause.hide()
                d.button_resume.hide()
                d.button_interrupt.hide()
            else:
                # check if thread is interrupted
                if event_thread_interrupt.isSet() is True:
                    # download interrupted
                    # show only resume button
                    d.button_pause.hide()
                    d.button_resume.show()
                    d.button_interrupt.hide()
                    # Interrupted
                    d.label_speed.setText('Interrupted')
                else:
                    # download active (or pause)
                    # show buttons
                    if speed >= 0:
                        d.button_pause.show()
                    d.button_interrupt.show()
                    d.button_resume.show()
                    # check download speed
                    if 0 <= speed < 1:
                        speedKb = str(round(speed * 1000, 1)) + ' KB/s'
                        d.label_speed.setText(speedKb) # download speed KB/s
                    elif speed >= 1:
                        speedMb = str(round(speed, 1)) + ' MB/s'
                        d.label_speed.setText(speedMb) # download speed MB/s
                    else:
                        # download paused
                        d.label_speed.setText('Paused')
                        d.button_pause.hide()

    # remove a specific downloadItem from ScrollArea
    @QtCore.pyqtSlot(list)
    def remove(self, list):
        # list contains downloadItemView, downloadItemController, uid
        downloadItemView = list[0]
        downloadItemController = list[1]
        uid = list[2]
        # we remove downloadItemView from downloadItems list
        self.model.downloadItems.remove((downloadItemView, uid))
        # we remove the respective controller from downloadItemsControllers list
        self.model.downloadItemsControllers.remove(downloadItemController)
        # we remove the downloadItemView from the scrollAreaWidgetLayout
        self.ui.scrollAreaWidgetLayout.removeWidget(downloadItemView)
        # we invoke the destructor. it's necessary to avoid problem with child of downloadItemView
        sip.delete(downloadItemView)
        list[0] = None
