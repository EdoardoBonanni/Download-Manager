class tableItem:
    def __init__(self, uid, tableitem_id, filename, status, dimension, start_time, end_time):
        self.uid = uid
        self.tableitem_id = tableitem_id
        self.filename = filename
        self.status = status
        self.dimension = dimension
        self.start_time = start_time
        self.end_time = end_time


    def updateValues(self, filename, status, dimension, start_time, end_time):
        self.filename = filename
        self.status = status
        self.dimension = dimension
        self.start_time = start_time
        self.end_time = end_time


    def getValues(self):
        return [self.uid, self.tableitem_id, self.filename, self.status, self.dimension, self.start_time, self.end_time]
