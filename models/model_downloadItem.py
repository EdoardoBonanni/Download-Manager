class Model_downloadItem:
    # model for downloadItem
    def __init__(self, downloadItemView, link, dir, filename, signalControllerMW, event_thread_pause, event_thread_interrupt, uid, fileDownload_object, event_thread_remove, signalControllerHistory, tableItem, bytes_read, total_bytes):
        # a reference to the downloadItemView object
        self.downloadItemView = downloadItemView
        # link download
        self.link = link
        # directory download
        self.dir = dir
        # filename download
        self.filename = filename
        # a reference to the signalControllerMainWindow object
        self.scMW = signalControllerMW
        # event thread indicating if download is in pause
        self.event_thread_pause = event_thread_pause
        # event thread indicating if download is interruted
        self.event_thread_interrupt = event_thread_interrupt
        # unique id thread/download
        self.uid = uid
        # fileDownload object
        self.fileDownload_object = fileDownload_object
        # event thread indicating if download is removed
        self.event_thread_remove = event_thread_remove
        # a reference to the signalControllerHistory object
        self.sch = signalControllerHistory
        # a reference to the tableItem object
        self.ti = tableItem
        # bytes of file downloaded overall
        self.bytes_read = bytes_read
        # total bytes of download
        self.total_bytes = total_bytes
