from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
from views.historyView import Ui_history


class signalControllerHistory(QDialog):
    def __init__(self, parent=None):
        super(signalControllerHistory, self).__init__(parent)

        self.ui = Ui_history()
        self.ui.setupUi(self)

        self.items = []
        self.status_array = []
        self.end_times = []


    @QtCore.pyqtSlot(list)
    def addTableItem(self, list):
        # in this case list contains only ti
        ti = list[0]
        # ti contains uid, tableitem_id, filename, status, dimension, start_time, end_time
        values = ti.getValues()
        idTableItems = [item[1] for item in self.items] # extract tableitem_id from tuple of items

        if values[1] not in idTableItems: # check if a particular download exist
            self.ui.tableWidget.insertRow(0) # add a row in position 0

            self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(values[2]))) # filename
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(values[3]))) # status
            self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(values[4]))) # dimension
            self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(values[5]))) # start_time
            self.ui.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(values[6]))) # end_time

            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)
            self.ui.tableWidget.resizeColumnToContents(2)
            self.ui.tableWidget.resizeColumnToContents(3)
            self.ui.tableWidget.resizeColumnToContents(4)

            self.items.insert(0, (values[0], values[1], values[2], values[4], values[5])) # insert a tuple of (uid, tableitem_id, filename, dimension, start_time) in top of array = position 0
            # Because tuple is not subscriptable i need an array for every values of tableItem that can change
            self.status_array.insert(0, values[3])
            self.end_times.insert(0, values[6])


    @QtCore.pyqtSlot(list)
    def updateTableItem(self, list):
        # in this case list contains only ti
        ti = list[0]
        # ti contains uid, tableitem_id, filename, status, dimension, start_time, end_time
        values = ti.getValues()
        idTableItems = [item[1] for item in self.items] # extract tableitem_id from tuple of items

        if values[1] in idTableItems: # check if a particular download exist
            rowPosition = idTableItems.index(values[1]) # update a tableitem with the rowPosition
            self.ui.tableWidget.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(values[2]))) # filename
            self.ui.tableWidget.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(values[3]))) # status
            self.ui.tableWidget.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(values[4]))) # dimension
            self.ui.tableWidget.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(values[5]))) # start_time
            self.ui.tableWidget.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(values[6]))) # end_time

            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)
            self.ui.tableWidget.resizeColumnToContents(2)
            self.ui.tableWidget.resizeColumnToContents(3)
            self.ui.tableWidget.resizeColumnToContents(4)

            self.status_array[rowPosition] = values[3] # update status
            self.end_times[rowPosition] = values[6] # update end_time


    @QtCore.pyqtSlot(list)
    def readHistory(self, list):
        history_items = list[0]
        history_status = list[1]
        history_end_times = list[2]
        for i in range(len(history_items) - 1, -1, -1):
            self.ui.tableWidget.insertRow(0) # add a row in position 0

            item = history_items[i]
            uid = item[0]
            tableItem_id = item[1]
            filename = item[2]
            status = history_status[i]
            dimension = item[3]
            start_time = item[4]
            end_time = history_end_times[i]

            if (status == 'Started' or status == 'Restarted') and end_time == 'N/A':
                status = 'Interrupted'

            self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(filename))) # filename
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(status))) # status
            self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(dimension))) # dimension
            self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(start_time))) # start_time
            self.ui.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(end_time))) # end_time

            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)
            self.ui.tableWidget.resizeColumnToContents(2)
            self.ui.tableWidget.resizeColumnToContents(3)
            self.ui.tableWidget.resizeColumnToContents(4)

            self.items.insert(0, (uid, tableItem_id, filename, dimension, start_time)) # insert a tuple of (uid, tableitem_id, filename, dimension, start_time) in top of array = position 0
            # Because tuple is not subscriptable i need an array for every values of tableItem that can change
            self.status_array.insert(0, status)
            self.end_times.insert(0, end_time)


