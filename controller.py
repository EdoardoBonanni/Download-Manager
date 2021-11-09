from PyQt5.QtWidgets import QMainWindow
from MainWindow import Ui_mainWindow
from downloadItemView import downloadItem
from model import Model
import os
import utils

class Controller(QMainWindow):
    def __init__(self, model: Model):
        super(Controller, self).__init__()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.model = model

        self.searchInitialDir()
        self.show()
        self.actions()

    def actions(self):
        # choose directory event
        self.ui.button_browse.clicked.connect(self.chooseDirectory)
        self.ui.actionBrowse.triggered.connect(self.chooseDirectory)

        # download event
        self.ui.button_Download.clicked.connect(self.createDownloadItemView)
        #self.ui.button_Download.clicked.connect(self.download)
        self.ui.actionDownload.triggered.connect(self.download)


    def searchInitialDir(self):
        currdir = os.getcwd()
        currdir = currdir.replace('\\','/')
        self.ui.lineEdit_chooseDirectory.setText(currdir + '/downloads')

    def chooseDirectory(self):
        dir = self.ui.lineEdit_chooseDirectory.text()
        # print('Current directory Download:', dir)
        directorypath = self.model.chooseDirectory(dir)
        # print('New directory Download:', directorypath)
        self.ui.lineEdit_chooseDirectory.setText(directorypath)

    def download(self):
        self.ui.lineEdit_Download.setText('https://www.freewebheaders.com/wp-content/gallery/holidays-size-800x200_1/thumbs/thumbs_unique-multicolor-indian-christmas-ornaments-banner-background-800x200.jpg')
        link = self.ui.lineEdit_Download.text()
        if link != '':
            dir = self.ui.lineEdit_chooseDirectory.text()
            self.model.downloadFile(link, dir)

    def createDownloadItemView(self):
        file_name = 'sndsggydvwdguywdgywvyfgvywvywsvuicugcwucgucb.jpg'
        dimension = 111111111110 # bytes
        download_percentage = 99.3
        speed = '32.3 MB/s'

        # compute speed and dimension
        ## dimension
        d = utils.convert_size(dimension)

        downloadItem(self.ui, file_name, download_percentage, speed, d)





