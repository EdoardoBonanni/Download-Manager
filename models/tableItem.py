class tableItem:
    # values of a row of table_history
    def __init__(self, uid, tableitem_id, filename, status, dimension, start_time, end_time):
        # id unique of list of values
        self.uid = uid
        # id in the table
        self.tableitem_id = tableitem_id
        # name of file
        self.filename = filename
        # status of download
        self.status = status
        # dimension of download
        self.dimension = dimension
        # start time of download
        self.start_time = start_time
        # end time of download (if it's completed)
        self.end_time = end_time

    def updateValues(self, filename, status, dimension, start_time, end_time):
        # update all values (equivalent of set method)
        self.filename = filename
        self.status = status
        self.dimension = dimension
        self.start_time = start_time
        self.end_time = end_time

    def getValues(self):
        # return a list containing all values (equivalent of get method)
        return [self.uid, self.tableitem_id, self.filename, self.status, self.dimension, self.start_time, self.end_time]
