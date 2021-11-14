class Message:
    def __init__(self, message):
        self.message = message

    def receiveData(self):
        return self.message

    def changeData(self, data):
        self.message = data
