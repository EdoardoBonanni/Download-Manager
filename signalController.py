from PyQt5 import QtCore, QtGui, QtWidgets
from downloadItemView import downloadItemView
from MainWindow import Ui_mainWindow

class signalController(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.ui = mainWindow
        self.downloadItems = []

    @QtCore.pyqtSlot(list)
    def addDownload(self, list):
        # print("Adding a download widget")
        d = downloadItemView(list[0], list[1], list[2], list[3]) # list contains filename, download_percentage, speed, dimension, uid
        self.downloadItems.append((d, list[4]))
        self.ui.scrollAreaWidgetLayout.removeItem(self.ui.spacerVertical_downloadList)
        self.ui.scrollAreaWidgetLayout.addWidget(d)
        self.ui.scrollAreaWidgetLayout.addItem(self.ui.spacerVertical_downloadList)

    @QtCore.pyqtSlot(list)
    def updateDownloadValues(self, list):
        # print("Update upload values")
        # print(list)
        tupla = [item[0] for item in self.downloadItems if item[1] == list[4]] # search downloadItem with a specific uid
        d = tupla[0] # get downloadItemView
        # d.label_download_percentage.setText(str(list[1]) + '%')
        d.progressBar.setProperty("value", int(list[1]))
        if isinstance(list[2], str):
            d.label_speed.setText(list[2]) # download completed
        else:
            if list[2] < 1:
                speedKb = str(round(list[2] * 1000, 1)) + ' Kb/s'
                d.label_speed.setText(speedKb) # download speed Kb/s
            else:
                speedMb = str(round(list[2], 1)) + ' Mb/s'
                d.label_speed.setText(speedMb) # download speed Mb/s