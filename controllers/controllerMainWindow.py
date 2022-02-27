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
from models.model_history import Model_history
from models.model_MainWindow import Model_MainWindow

class controllerMainWindow(QMainWindow):
    # controller for MainWindow
    def __init__(self):
        # init UI
        super(controllerMainWindow, self).__init__()

        ui = Ui_mainWindow()
        ui.setupUi(self)

        # initialize timer
        self.timerHistory = QtCore.QTimer()
        # define model_history
        self.model_history = Model_history()
        # define model MainWindow
        self.model_mainwindow = Model_MainWindow()

        # start signalControllerMainWindow and signalControllerHistory
        self.scMW = signalControllerMainWindow(ui, self.model_mainwindow)
        self.controller_history = signalControllerHistory(self.model_history)

        # search initial dir for downloads
        self.searchInitialDir()
        # read history from file
        self.readHistory()
        # show the window and define the interactions
        self.show()
        self.interactions()


    def interactions(self):
        # events for choose download directory
        self.scMW.ui.button_browse.clicked.connect(self.chooseDirectory)
        self.scMW.ui.actionBrowse.triggered.connect(self.chooseDirectory)

        # events for start download
        self.scMW.ui.button_Download.clicked.connect(self.download)
        self.scMW.ui.actionDownload.triggered.connect(self.download)

        # events for close mainwindow
        self.scMW.ui.actionClose.triggered.connect(self.close_window)
        self.scMW.ui.actionHistory.triggered.connect(self.showHistory)

        # update history file every second with timer
        self.timerHistory.timeout.connect(self.updateHistoryFile)
        self.timerHistory.start(1000)


    def searchInitialDir(self):
        # search initial dir for downloads and insert the path in the line edit
        currdir = os.getcwd()
        currdir = currdir.replace('\\','/')
        self.scMW.ui.lineEdit_chooseDirectory.setText(currdir + '/downloads')


    def chooseDirectory(self):
        # choose new directory for downloads
        dir = self.scMW.ui.lineEdit_chooseDirectory.text()
        #print('Current directory Download:', dir)
        directorypath = utils_function.chooseDirectory(dir)
        #print('New directory Download:', directorypath)
        self.scMW.ui.lineEdit_chooseDirectory.setText(directorypath)


    def download(self):
        # function that start a new thread for download
        link = self.scMW.ui.lineEdit_Download.text()
        dir = self.scMW.ui.lineEdit_chooseDirectory.text()
        # initilize the thread
        download = fileDownload()
        # wait a moment
        time.sleep(0.2)
        # start the thread
        download.check_download_info(link, dir, self.scMW, self.controller_history)
        self.scMW.ui.lineEdit_Download.setText('')


    def showHistory(self):
        # show the history
        self.controller_history.show()


    def readHistory(self):
        # read the history from pickle file (if exist)
        if os.path.isfile('history_files/historyItems.pkl'):
            history = save_load_object.loadObject('history_files/historyItems')
            # update the history view with a signal
            messageHistory = Message(history)
            signalHistory = Signal(messageHistory)
            signalHistory.messageChanged.connect(self.controller_history.readHistory)
            signalHistory.start()
            messageHistory = None
            signalHistory = None


    def updateHistoryFile(self):
        # update (or create) history pickle file
        listHistory = [self.model_history.items, self.model_history.status_array, self.model_history.end_times]
        save_load_object.saveObject(listHistory, 'history_files/historyItems')


    def close_window(self):
        # close window and update history pickle file
        listHistory = [self.model_history.items, self.model_history.status_array, self.model_history.end_times]
        save_load_object.saveObject(listHistory, 'history_files/historyItems')
        sys.exit()


    # override of close event
    def closeEvent(self, event):
        # close window and update history pickle file
        listHistory = [self.model_history.items, self.model_history.status_array, self.model_history.end_times]
        save_load_object.saveObject(listHistory, 'history_files/historyItems')
        sys.exit()






