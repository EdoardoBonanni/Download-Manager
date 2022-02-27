class Message:
    # class that define a message that can be send from thread to controllers to update the views
    def __init__(self, message):
        self.message = message

    def receiveData(self):
        # return the message (equivalent of get method)
        return self.message

    def changeData(self, data):
        # update the message (equivalent of set method)
        self.message = data
