from PyQt5 import QtCore, QtGui, QtWidgets
from downloadItemView import downloadItemView
from MainWindow import Ui_mainWindow

class signalController(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.ui = mainWindow
        self.d = None

    @QtCore.pyqtSlot(list)
    def addDownload(self, list):
        print("Adding a download widget")
        self.d = downloadItemView(list[0], list[1], list[2], list[3]) # list contains filename, download_percentage, speed, dimension
        self.ui.scrollAreaWidgetLayout.removeItem(self.ui.spacerVertical_downloadList)
        self.ui.scrollAreaWidgetLayout.addWidget(self.d)
        self.ui.scrollAreaWidgetLayout.addItem(self.ui.spacerVertical_downloadList)

    @QtCore.pyqtSlot(list)
    def updateDownloadValues(self, list):
        print("Update upload values")
        # print(list)
        self.d.label_download_percentage.setText(str(list[1]) + '%')
        if isinstance(list[2], str):
            self.d.label_speed.setText(list[2]) # download finished
        else:
            self.d.label_speed.setText(str(list[2]) + ' Mbps') # download speed