from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_history(object):
    def setupUi(self, historydialog):

        # historydialog
        historydialog.setObjectName("historydialog")
        historydialog.resize(900, 650)
        historydialog.setMinimumSize(QtCore.QSize(900, 650))
        historydialog.setBaseSize(QtCore.QSize(900, 650))

        # gridlayout and tablewidget
        self.gridLayout = QtWidgets.QGridLayout(historydialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(historydialog)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)

        # font header
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        # icon
        icon_mainwindow = QtGui.QIcon()
        icon_mainwindow.addPixmap(QtGui.QPixmap("../icon/download-icon-mainwindow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        historydialog.setWindowIcon(icon_mainwindow)

        # header table
        item0 = QtWidgets.QTableWidgetItem()
        item0.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item0)
        item1 = QtWidgets.QTableWidgetItem()
        item1.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item1)
        item2 = QtWidgets.QTableWidgetItem()
        item2.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item2)
        item3 = QtWidgets.QTableWidgetItem()
        item3.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item3)
        item4 = QtWidgets.QTableWidgetItem()
        item4.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item4)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.retranslateUi(historydialog)
        QtCore.QMetaObject.connectSlotsByName(historydialog)


    def retranslateUi(self, historydialog):
        _translate = QtCore.QCoreApplication.translate
        historydialog.setWindowTitle(_translate("historydialog", "Download Manager History"))
        self.tableWidget.setSortingEnabled(False)
        item0 = self.tableWidget.horizontalHeaderItem(0)
        item0.setText(_translate("historydialog", "Filename"))
        item1 = self.tableWidget.horizontalHeaderItem(1)
        item1.setText(_translate("historydialog", "Status"))
        item2 = self.tableWidget.horizontalHeaderItem(2)
        item2.setText(_translate("historydialog", "Dimension"))
        item3 = self.tableWidget.horizontalHeaderItem(3)
        item3.setText(_translate("historydialog", "Time Started"))
        item4 = self.tableWidget.horizontalHeaderItem(4)
        item4.setText(_translate("historydialog", "Time Completed/aborted"))



