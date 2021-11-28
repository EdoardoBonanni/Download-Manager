from PyQt5 import QtCore, QtGui, QtWidgets
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

        self.timer = QtCore.QTimer()

        self.scMW = signalControllerMainWindow(ui)
        self.controller_history = signalControllerHistory()

        self.searchInitialDir()
        self.readHistory()
        self.show()
        self.actions()



    def actions(self):
        # choose directory event
        self.scMW.ui.button_browse.clicked.connect(self.chooseDirectory)
        self.scMW.ui.actionBrowse.triggered.connect(self.chooseDirectory)

        # download event
        self.scMW.ui.button_Download.clicked.connect(self.download)
        self.scMW.ui.actionDownload.triggered.connect(self.download)

        # close mainwindow event
        self.scMW.ui.actionClose.triggered.connect(self.close_window)
        self.scMW.ui.actionHistory.triggered.connect(self.showHistory)

        # update history file every second
        self.timer.timeout.connect(self.updateHistoryFile)
        self.timer.start(1000)

    def searchInitialDir(self):
        currdir = os.getcwd()
        currdir = currdir.replace('\\','/')
        self.scMW.ui.lineEdit_chooseDirectory.setText(currdir + '/downloads')

    def chooseDirectory(self):
        dir = self.scMW.ui.lineEdit_chooseDirectory.text()
        # print('Current directory Download:', dir)
        directorypath = utils_function.chooseDirectory(dir)
        # print('New directory Download:', directorypath)
        self.scMW.ui.lineEdit_chooseDirectory.setText(directorypath)

    def download(self):
        link = self.scMW.ui.lineEdit_Download.text()
        dir = self.scMW.ui.lineEdit_chooseDirectory.text()
        download = fileDownload()
        time.sleep(0.2)
        download.check_download_info(link, dir, self.scMW, self.controller_history)

    def showHistory(self):
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

    def updateHistoryFile(self):
        list = [self.controller_history.items, self.controller_history.status_array, self.controller_history.end_times]
        save_load_object.saveObject(list, 'history_files/historyItems')

    def close_window(self):
        list = [self.controller_history.items, self.controller_history.status_array, self.controller_history.end_times]
        save_load_object.saveObject(list, 'history_files/historyItems')
        sys.exit()

    # override of close event
    def closeEvent(self, event):
        list = [self.controller_history.items, self.controller_history.status_array, self.controller_history.end_times]
        save_load_object.saveObject(list, 'history_files/historyItems')
        sys.exit()






