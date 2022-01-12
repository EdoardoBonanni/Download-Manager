from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

class downloadItemView(QWidget):

    def __init__(self, file_name, download_percentage, speed, dimension):
        super().__init__()

        font = QtGui.QFont()
        font.setPointSize(8)
        self.setFont(font)
        self.setObjectName("horizontalWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # label_name
        self.label_name = QtWidgets.QLabel(self)
        fontName = QtGui.QFont()
        fontName.setPointSize(10)
        self.label_name.setFont(fontName)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout.addWidget(self.label_name)

        # label_speed
        self.label_speed = QtWidgets.QLabel(self)
        self.label_speed.setObjectName("label_speed")
        self.horizontalLayout.addWidget(self.label_speed)

        # progressbar
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setProperty("value", download_percentage)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)

        # label_dimension
        self.label_dimension = QtWidgets.QLabel(self)
        self.label_dimension.setObjectName("label_dimension")
        self.horizontalLayout.addWidget(self.label_dimension)

        # button pause, resume, interrupt
        self.button_pause = QtWidgets.QPushButton(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_pause.setIcon(icon)
        self.button_pause.setObjectName("button_pause")
        self.horizontalLayout.addWidget(self.button_pause)
        self.button_resume= QtWidgets.QPushButton(self)
        iconResume = QtGui.QIcon()
        iconResume.addPixmap(QtGui.QPixmap("icon/resume.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_resume.setIcon(iconResume)
        self.button_resume.setObjectName("button_resume")
        self.button_resume.setStyleSheet('background-color: #008500; border-color: #008500; color:#ffffff')
        self.horizontalLayout.addWidget(self.button_resume)
        self.button_interrupt = QtWidgets.QPushButton(self)
        iconInterrupt = QtGui.QIcon()
        iconInterrupt.addPixmap(QtGui.QPixmap("icon/interrupt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_interrupt.setIcon(iconInterrupt)
        self.button_interrupt.setObjectName("button_interrupt")
        self.button_interrupt.setStyleSheet('background-color: #D60000; border-color: #D60000; color:#ffffff')
        self.horizontalLayout.addWidget(self.button_interrupt)

        # button remove
        iconRemove = QtGui.QIcon()
        iconRemove.addPixmap(QtGui.QPixmap("icon/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove = QtWidgets.QPushButton(self)
        self.button_remove.setIcon(iconRemove)
        self.button_remove.setObjectName("button_remove")
        self.button_remove.setStyleSheet('background-color: #000000; border-color: #000000; color:#ffffff')
        self.horizontalLayout.addWidget(self.button_remove)
        self.horizontalLayout.setStretch(0, 10)

        # traslate
        _translate = QtCore.QCoreApplication.translate
        self.label_name.setText(_translate("MainWindow", file_name))
        self.label_speed.setText(_translate("MainWindow", str(round(float(speed), 1)) + ' KB/s'))
        self.label_dimension.setText(_translate("MainWindow", dimension))

        self.setLayout(self.horizontalLayout)




