from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    # Mainwindow view
    def setupUi(self, mainWindow):

        # mainwindow properties
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(900, 650)
        mainWindow.setMinimumSize(QtCore.QSize(900, 650))
        mainWindow.setBaseSize(QtCore.QSize(900, 650))
        font = QtGui.QFont()
        font.setPointSize(10)
        mainWindow.setFont(font)
        fontLineEdit = QtGui.QFont()
        fontLineEdit.setPointSize(8)

        # icon of window
        icon_mainwindow = QtGui.QIcon()
        icon_mainwindow.addPixmap(QtGui.QPixmap("icon/download-icon-mainwindow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon_mainwindow)
        iconDownload = QtGui.QIcon()
        iconDownload.addPixmap(QtGui.QPixmap("icon/download.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        iconExit = QtGui.QIcon()
        iconExit.addPixmap(QtGui.QPixmap("icon/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        iconBrowse = QtGui.QIcon()
        iconBrowse.addPixmap(QtGui.QPixmap("icon/browse.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        iconHistory = QtGui.QIcon()
        iconHistory.addPixmap(QtGui.QPixmap("icon/History.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # centralwidget and gridlayout
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # widget_containing_scrollArea and layout_containing_scrollArea
        self.widget_containing_scrollArea = QtWidgets.QWidget(self.centralwidget)
        self.widget_containing_scrollArea.setObjectName("widget_containing_scrollArea")
        self.layout_containing_scrollArea = QtWidgets.QVBoxLayout(self.widget_containing_scrollArea)
        self.layout_containing_scrollArea.setContentsMargins(10, 10, 10, 10)
        self.layout_containing_scrollArea.setObjectName("layout_containing_scrollArea")
        ## scrollArea
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaLayout = QtWidgets.QHBoxLayout(self.scrollArea)
        self.scrollAreaLayout.setContentsMargins(100, 100, 100, 100)
        self.scrollAreaLayout.setObjectName("scrollAreaLayout")
        ### scrollAreaWidgetContents and scrollAreaWidgetLayout
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 863, 437))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetLayout.setObjectName("scrollAreaWidgetLayout")
        ### verticalSpacer
        self.spacerVertical_downloadList = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scrollAreaWidgetLayout.addItem(self.spacerVertical_downloadList)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout_containing_scrollArea.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.widget_containing_scrollArea, 2, 0, 1, 1)

        # widget_download
        self.widget_download = QtWidgets.QWidget(self.centralwidget)
        self.widget_download.setObjectName("widget_download")
        self.horizontalLayout_Download = QtWidgets.QHBoxLayout(self.widget_download)
        self.horizontalLayout_Download.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_Download.setObjectName("horizontalLayout_Download")
        self.label_insertDownload = QtWidgets.QLabel(self.widget_download)
        self.label_insertDownload.setObjectName("label_insertDownload")
        self.horizontalLayout_Download.addWidget(self.label_insertDownload)
        spacerItem_downloadLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_Download.addItem(spacerItem_downloadLeft)
        self.lineEdit_Download = QtWidgets.QLineEdit(self.widget_download)
        self.lineEdit_Download.setObjectName("lineEdit_Download")
        self.lineEdit_Download.setFont(fontLineEdit)
        self.horizontalLayout_Download.addWidget(self.lineEdit_Download)
        spacerItem_downloadRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_Download.addItem(spacerItem_downloadRight)
        self.button_Download = QtWidgets.QPushButton(self.widget_download)
        self.button_Download.setMaximumSize(QtCore.QSize(130, 24))
        self.button_Download.setObjectName("pushButton_Download")
        self.horizontalLayout_Download.addWidget(self.button_Download)
        self.horizontalLayout_Download.setStretch(0, 4)
        self.horizontalLayout_Download.setStretch(2, 12)
        self.horizontalLayout_Download.setStretch(4, 2)
        self.gridLayout.addWidget(self.widget_download, 0, 0, 1, 1)

        # widget_browse
        self.widget_browse = QtWidgets.QWidget(self.centralwidget)
        self.widget_browse.setObjectName("widget_browse")
        self.horizontalLayout_Browse = QtWidgets.QHBoxLayout(self.widget_browse)
        self.horizontalLayout_Browse.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_Browse.setObjectName("horizontalLayout_Browse")
        self.label_chooseDirectory = QtWidgets.QLabel(self.widget_browse)
        self.label_chooseDirectory.setObjectName("label_chooseDirectory")
        self.horizontalLayout_Browse.addWidget(self.label_chooseDirectory)
        spacerItem_browseLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_Browse.addItem(spacerItem_browseLeft)
        self.lineEdit_chooseDirectory = QtWidgets.QLineEdit(self.widget_browse)
        self.lineEdit_chooseDirectory.setObjectName("lineEdit_chooseDirectory")
        self.lineEdit_chooseDirectory.setFont(fontLineEdit)
        self.horizontalLayout_Browse.addWidget(self.lineEdit_chooseDirectory)
        spacerItem_browseRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_Browse.addItem(spacerItem_browseRight)
        self.button_browse = QtWidgets.QPushButton(self.widget_browse)
        self.button_browse.setMaximumSize(QtCore.QSize(130, 24))
        self.button_browse.setObjectName("pushButton_browse")
        self.horizontalLayout_Browse.addWidget(self.button_browse)
        self.horizontalLayout_Browse.setStretch(0, 4)
        self.horizontalLayout_Browse.setStretch(2, 12)
        self.horizontalLayout_Browse.setStretch(4, 2)
        self.gridLayout.addWidget(self.widget_browse, 1, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.button_Download.setStyleSheet('background-color: #ffc107; border-color: #ffc107')
        self.button_browse.setStyleSheet('background-color: #ffc107; border-color: #ffc107')

        # menubar
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionDownload = QtWidgets.QAction(mainWindow)
        self.actionDownload.setIcon(iconDownload)
        self.actionDownload.setObjectName("actionDownload")
        self.actionClose = QtWidgets.QAction(mainWindow)
        self.actionClose.setIcon(iconExit)
        self.actionClose.setObjectName("actionExit")
        self.actionBrowse = QtWidgets.QAction(mainWindow)
        self.actionBrowse.setIcon(iconBrowse)
        self.actionBrowse.setObjectName("actionBrowse")
        self.actionHistory = QtWidgets.QAction(mainWindow)
        self.actionHistory.setIcon(iconHistory)
        self.actionHistory.setObjectName("actionHistory")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionDownload)
        self.menuFile.addAction(self.actionBrowse)
        self.menuFile.addAction(self.actionHistory)
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)


    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Download Manager"))
        self.label_insertDownload.setText(_translate("mainWindow", "Insert URL File to Download"))
        self.button_Download.setText(_translate("mainWindow", "Download"))
        self.label_chooseDirectory.setText(_translate("mainWindow", "Choose directory to save files"))
        self.button_browse.setText(_translate("mainWindow", "Browse"))
        self.menuFile.setTitle(_translate("mainWindow", "&File"))
        self.actionDownload.setText(_translate("mainWindow", "&Download"))
        self.actionDownload.setShortcut(_translate("mainWindow", "Ctrl+D"))
        self.actionDownload.setStatusTip(_translate("mainWindow", "Download a file"))
        self.actionClose.setText(_translate("mainWindow", "&Close"))
        self.actionClose.setShortcut(_translate("mainWindow", "Ctrl+Z"))
        self.actionClose.setStatusTip(_translate("mainWindow", "Close"))
        self.actionBrowse.setText(_translate("mainWindow", "&Browse"))
        self.actionBrowse.setShortcut(_translate("mainWindow", "Ctrl+B"))
        self.actionBrowse.setStatusTip(_translate("mainWindow", "Browse a file"))
        self.actionHistory.setText(_translate("mainWindow", "&History"))
        self.actionHistory.setShortcut(_translate("mainWindow", "Ctrl+H"))
        self.actionHistory.setStatusTip(_translate("mainWindow", "View History"))










