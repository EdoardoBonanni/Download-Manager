from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

class downloadItem(QWidget):

    def __init__(self, ui, file_name, download_percentage, speed, dimension):
        super().__init__()
        self.ui = ui

        # horizontal layout and horizontal widget
        self.horizontalWidget = QtWidgets.QWidget()
        self.horizontalWidget.setMaximumSize(QtCore.QSize(16777215, 60))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.horizontalWidget.setFont(font)
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # labels
        self.label_name = QtWidgets.QLabel(self.horizontalWidget)
        fontName = QtGui.QFont()
        fontName.setPointSize(10)
        self.label_name.setFont(fontName)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)
        self.label_download_percentage = QtWidgets.QLabel(self.horizontalWidget)
        self.label_download_percentage.setObjectName("label_download_percentage")
        self.horizontalLayout.addWidget(self.label_download_percentage)
        self.label_speed = QtWidgets.QLabel(self.horizontalWidget)
        self.label_speed.setObjectName("label_speed")
        self.horizontalLayout.addWidget(self.label_speed)
        self.label_dimension = QtWidgets.QLabel(self.horizontalWidget)
        self.label_dimension.setObjectName("label_dimension")
        self.horizontalLayout.addWidget(self.label_dimension)

        # button pause, resume, interrupt
        self.button_pause = QtWidgets.QPushButton(self.horizontalWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_pause.setIcon(icon)
        self.button_pause.setObjectName("button_pause")
        self.horizontalLayout.addWidget(self.button_pause)
        self.button_resume= QtWidgets.QPushButton(self.horizontalWidget)
        iconResume = QtGui.QIcon()
        iconResume.addPixmap(QtGui.QPixmap("icon/resume.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_resume.setIcon(iconResume)
        self.button_resume.setObjectName("button_resume")
        self.button_resume.setStyleSheet('background-color: #008500; border-color: #008500; color:#fff')
        self.horizontalLayout.addWidget(self.button_resume)
        self.button_interrupt = QtWidgets.QPushButton(self.horizontalWidget)
        iconInterrupt = QtGui.QIcon()
        iconInterrupt.addPixmap(QtGui.QPixmap("icon/interrupt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_interrupt.setIcon(iconInterrupt)
        self.button_interrupt.setObjectName("button_interrupt")
        self.button_interrupt.setStyleSheet('background-color: #D60000; border-color: #D60000; color:#fff')
        self.horizontalLayout.addWidget(self.button_interrupt)

        # button remove
        iconRemove = QtGui.QIcon()
        iconRemove.addPixmap(QtGui.QPixmap("icon/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove = QtWidgets.QPushButton(self.horizontalWidget)
        self.button_remove.setIcon(iconRemove)
        self.button_remove.setObjectName("button_remove")
        self.horizontalLayout.addWidget(self.button_remove)
        self.horizontalLayout.setStretch(0, 10)

        # traslate
        _translate = QtCore.QCoreApplication.translate
        self.label_name.setText(_translate("MainWindow", file_name))
        self.label_download_percentage.setText(_translate("MainWindow", str(download_percentage) + '%'))
        self.label_speed.setText(_translate("MainWindow", speed))
        self.label_dimension.setText(_translate("MainWindow", dimension))
        self.button_pause.setText(_translate("MainWindow", "Pause"))
        self.button_resume.setText(_translate("MainWindow", "Resume"))
        self.button_interrupt.setText(_translate("MainWindow", "Interrupt"))
        self.button_remove.setText(_translate("MainWindow", "Remove"))

        self.ui.verticalLayout_ListDownload.removeItem(self.ui.spacerVertical_downloadList)
        self.ui.verticalLayout_ListDownload.update()
        self.ui.verticalLayout_ListDownload.addWidget(self.horizontalWidget)
        self.ui.verticalLayout_ListDownload.update()
        self.ui.verticalLayout_ListDownload.addItem(self.ui.spacerVertical_downloadList)
        self.ui.verticalLayout_ListDownload.update()



