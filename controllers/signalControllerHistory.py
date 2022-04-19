from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
from views.historyView import Ui_history
from models.model_history import Model_history

class signalControllerHistory(QDialog):
    # controller for history QDialog
    def __init__(self, model: Model_history, parent=None):
        super(signalControllerHistory, self).__init__(parent)

        self.ui = Ui_history()
        self.ui.setupUi(self)

        # model_history
        self.model = model


    @QtCore.pyqtSlot(list)
    def addTableItem(self, list):
        # in this case list contains only ti
        ti = list[0]
        # ti contains uid, tableitem_id, filename, status, dimension, start_time, end_time
        values = ti.getValues()
        uid = values[0]
        tableitem_id = values[1]
        filename = values[2]
        status = values[3]
        dimension = values[4]
        start_time = values[5]
        end_time = values[6]
        # extract tableitem_id from tuple of items
        idTableItems = [item[1] for item in self.model.items]
        # check if a particular download exist
        if tableitem_id not in idTableItems:
            # add a row in position 0
            self.ui.tableWidget.insertRow(0)

            # add values to table row items
            self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(filename)))
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(status)))
            self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(dimension)))
            self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(start_time)))
            self.ui.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(end_time)))

            # resize columns of table
            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)
            self.ui.tableWidget.resizeColumnToContents(2)
            self.ui.tableWidget.resizeColumnToContents(3)
            self.ui.tableWidget.resizeColumnToContents(4)

            # insert a tuple of (uid, tableitem_id, filename, dimension, start_time) in top of array = position 0
            self.model.items.insert(0, (uid, tableitem_id, filename, dimension, start_time))
            # Because tuple is not subscriptable I need an array for every values of tableItem that can change (status and end_times)
            # So, I insert these values in the following lists
            self.model.status_array.insert(0, status)
            self.model.end_times.insert(0, end_time)


    @QtCore.pyqtSlot(list)
    def updateTableItem(self, list):
        # in this case list contains only ti
        ti = list[0]
        # ti contains uid, tableitem_id, filename, status, dimension, start_time, end_time
        values = ti.getValues()
        tableitem_id = values[1]
        filename = values[2]
        status = values[3]
        dimension = values[4]
        start_time = values[5]
        end_time = values[6]
        # extract tableitem_id from tuple of items
        idTableItems = [item[1] for item in self.model.items]
        # check if a particular download exist
        if tableitem_id in idTableItems:
            # update a tableitem with the rowPosition
            rowPosition = idTableItems.index(values[1])

            # add values to table row items
            self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(filename)))
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(status)))
            self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(dimension)))
            self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(start_time)))
            self.ui.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(end_time)))

            # resize columns of table
            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)
            self.ui.tableWidget.resizeColumnToContents(2)
            self.ui.tableWidget.resizeColumnToContents(3)
            self.ui.tableWidget.resizeColumnToContents(4)

            self.model.status_array[rowPosition] = status # update status list
            self.model.end_times[rowPosition] = end_time # update end_time list


    @QtCore.pyqtSlot(list)
    def readHistory(self, list):
        # list contains history_items, history_status, history_end_times
        history_items = list[0]
        history_status = list[1]
        history_end_times = list[2]
        for i in range(len(history_items) - 1, -1, -1):
            # add a row in position 0 (for every download to fill the table)
            self.ui.tableWidget.insertRow(0)

            # read the values
            item = history_items[i]
            uid = item[0]
            tableItem_id = item[1]
            filename = item[2]
            status = history_status[i]
            dimension = item[3]
            start_time = item[4]
            end_time = history_end_times[i]

            # control if download was interrupted
            if (status == 'Started' or status == 'Paused' or status == 'Resumed' or status == 'Restarted') and end_time == 'N/A':
                status = 'Interrupted'

            # add values to table row items
            self.ui.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(filename)))
            self.ui.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(status)))
            self.ui.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(str(dimension)))
            self.ui.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(str(start_time)))
            self.ui.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(str(end_time)))

            # resize columns of table
            self.ui.tableWidget.resizeColumnToContents(0)
            self.ui.tableWidget.resizeColumnToContents(1)
            self.ui.tableWidget.resizeColumnToContents(2)
            self.ui.tableWidget.resizeColumnToContents(3)
            self.ui.tableWidget.resizeColumnToContents(4)

            # insert a tuple of (uid, tableitem_id, filename, dimension, start_time) in top of array = position 0
            self.model.items.insert(0, (uid, tableItem_id, filename, dimension, start_time))
            # Because tuple is not subscriptable i need an array for every values of tableItem that can change
            self.model.status_array.insert(0, status) # update status list
            self.model.end_times.insert(0, end_time) # update end_time list


