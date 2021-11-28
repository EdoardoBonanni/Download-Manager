from PyQt5.QtWidgets import QMainWindow
from views.MainWindow import Ui_mainWindow
from controllers.signalControllerMainWindow import signalControllerMainWindow
from fileDownload.fileDownload import fileDownload
import os, sys
from utils import utils_function, save_load_object
from controllers.signalControllerHistory import signalControllerHistory
import time
from utils.message import Message
from threadSignal.signal import Signal

class controllerMainWindow(QMainWindow):
    def __init__(self):
        super(controllerMainWindow, self).__init__()

        ui = Ui_mainWindow()
        ui.setupUi(self)
        self.sc = signalControllerMainWindow(ui)
        self.controller_history = signalControllerHistory()

        self.searchInitialDir()
        self.readHistory()
        self.show()
        self.actions()

    def actions(self):
        # choose directory event
        self.sc.ui.button_browse.clicked.connect(self.chooseDirectory)
        self.sc.ui.actionBrowse.triggered.connect(self.chooseDirectory)

        # download event
        self.sc.ui.button_Download.clicked.connect(self.download)
        self.sc.ui.actionDownload.triggered.connect(self.download)

        # close mainwindow event
        self.sc.ui.actionClose.triggered.connect(self.close)
        self.sc.ui.actionHistory.triggered.connect(self.showHistory)

    def searchInitialDir(self):
        currdir = os.getcwd()
        currdir = currdir.replace('\\','/')
        self.sc.ui.lineEdit_chooseDirectory.setText(currdir + '/downloads')

    def chooseDirectory(self):
        dir = self.sc.ui.lineEdit_chooseDirectory.text()
        # print('Current directory Download:', dir)
        directorypath = utils_function.chooseDirectory(dir)
        # print('New directory Download:', directorypath)
        self.sc.ui.lineEdit_chooseDirectory.setText(directorypath)

    def download(self):
        link = self.sc.ui.lineEdit_Download.text()
        dir = self.sc.ui.lineEdit_chooseDirectory.text()
        download = fileDownload()
        time.sleep(0.2)
        download.check_download_info(link, dir, self.sc, self.controller_history)

    def showHistory(self):
        print('history')
        self.controller_history.show()

    def readHistory(self):
        if os.path.isfile('history_files/historyItems.pkl'):
            history = save_load_object.loadObject('history_files/historyItems')
            messageHistory = Message(history)
            signalHistory = Signal(messageHistory)
            signalHistory.messageChanged.connect(self.controller_history.readHistory)
            signalHistory.start()
            messageHistory = None
            signalHistory = None

    def close(self):
        list = [self.controller_history.items, self.controller_history.status_array, self.controller_history.end_times]
        save_load_object.saveObject(list, 'history_files/historyItems')
        sys.exit()

    # override
    def closeEvent(self, event):
        list = [self.controller_history.items, self.controller_history.status_array, self.controller_history.end_times]
        save_load_object.saveObject(list, 'history_files/historyItems')
        sys.exit()






