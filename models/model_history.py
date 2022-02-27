class Model_history:
    # model for history view
    def __init__(self):
        # list that contains items of table (list of downloads started, completed and interrupted)
        self.items = []

        # list that contains the status of downloads
        self.status_array = []

        # list that contains the end_times of all downloads (used for determine if download is started but not completed)
        self.end_times = []
