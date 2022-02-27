class Model_MainWindow:
    # model for MainWindow
    def __init__(self):
        # a list of download started, paused, interrupted or completed
        self.downloadItems = []

        # a list of controllers of previous downloads
        self.downloadItemsControllers = []
