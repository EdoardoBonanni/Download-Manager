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
        self.ui = signalController(ui)

        self.searchInitialDir()
        self.show()
        self.actions()

    def actions(self):
        # choose directory event
        self.ui.ui.button_browse.clicked.connect(self.chooseDirectory)
        self.ui.ui.actionBrowse.triggered.connect(self.chooseDirectory)

        # download event
        self.ui.ui.button_Download.clicked.connect(self.download)
        self.ui.ui.actionDownload.triggered.connect(self.download)

    def searchInitialDir(self):
        currdir = os.getcwd()
        currdir = currdir.replace('\\','/')
        self.ui.ui.lineEdit_chooseDirectory.setText(currdir + '/downloads')

    def chooseDirectory(self):
        dir = self.ui.ui.lineEdit_chooseDirectory.text()
        # print('Current directory Download:', dir)
        directorypath = utils.chooseDirectory(dir)
        # print('New directory Download:', directorypath)
        self.ui.ui.lineEdit_chooseDirectory.setText(directorypath)

    def download(self):
        self.ui.ui.lineEdit_Download.setText('https://www.freewebheaders.com/wp-content/gallery/holidays-size-800x200_1/thumbs/thumbs_unique-multicolor-indian-christmas-ornaments-banner-background-800x200.jpg')
        # self.ui.ui.lineEdit_Download.setText('http://ipv4.download.thinkbroadband.com/200MB.zip')
        link = self.ui.ui.lineEdit_Download.text()
        dir = self.ui.ui.lineEdit_chooseDirectory.text()
        download = Download()
        download.check_download_info(link, dir, self.ui)
        print('fine')

    # def createDownloadItemView(self):
    #     file_name = 'sndsggydvwdguywdgywvyfgvywvywsvuicugcwucgucb.jpg'
    #     dimension = 111111111110 # bytes
    #     download_percentage = 99.3
    #     speed = 20.7
    #
    #     # compute speed and dimension
    #     ## dimension
    #     d = utils.convert_size(dimension)
    #
    #     diview = downloadItemView(file_name, download_percentage, speed, d)
    #
    #     self.ui.ui.changeView(diview)






