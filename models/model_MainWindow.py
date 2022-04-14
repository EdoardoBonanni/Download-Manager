class Model_MainWindow:
    # model for MainWindow
    def __init__(self):
        # a list of downloads started, paused, interrupted or completed
        self.downloadItems = []

        # a list of controllers of previous downloads
        self.downloadItemsControllers = []
