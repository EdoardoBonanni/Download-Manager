from PyQt5.QtWidgets import QMainWindow
from MainWindow import Ui_mainWindow
from signalController import signalController
from downloadItemView import downloadItemView
from download import Download
import os
import utils

class Controller(QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()

        ui = Ui_mainWindow()
        ui.setupUi(self)
        self.sc = signalController(ui)

        self.searchInitialDir()
        self.show()
        self.actions()

    def actions(self):
        # choose directory event
        self.sc.ui.button_browse.clicked.connect(self.chooseDirectory)
        self.sc.ui.actionBrowse.triggered.connect(self.chooseDirectory)

        # download event
        self.sc.ui.button_Download.clicked.connect(self.download)
        self.sc.ui.actionDownload.triggered.connect(self.download)

    def searchInitialDir(self):
        currdir = os.getcwd()
        currdir = currdir.replace('\\','/')
        self.sc.ui.lineEdit_chooseDirectory.setText(currdir + '/downloads')

    def chooseDirectory(self):
        dir = self.sc.ui.lineEdit_chooseDirectory.text()
        # print('Current directory Download:', dir)
        directorypath = utils.chooseDirectory(dir)
        # print('New directory Download:', directorypath)
        self.sc.ui.lineEdit_chooseDirectory.setText(directorypath)

    def download(self):
        # self.sc.ui.lineEdit_Download.setText('https://images.pexels.com/photos/5775/calculator-scientific.jpg')
        # self.sc.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/5MB.zip')
        # self.sc.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/10MB.zip')
        # self.sc.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/20MB.zip')
        self.sc.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/50MB.zip')
        # self.sc.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/100MB.zip')
        # self.sc.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/200MB.zip')
        link = self.sc.ui.lineEdit_Download.text()
        dir = self.sc.ui.lineEdit_chooseDirectory.text()
        download = Download()
        download.check_download_info(link, dir, self.sc)





