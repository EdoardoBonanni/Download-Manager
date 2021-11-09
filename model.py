import tkinter as tk
from tkinter import filedialog, messagebox
import os, requests

class Model:
    def __init__(self):
        # list of images
        self.downloads = list()
        self.activeDownloads = list()


    def chooseDirectory(self, initialdir):
        root = tk.Tk()
        root.withdraw() # use to hide tkinter window

        tempdir = filedialog.askdirectory(parent=root, initialdir=initialdir, title='Please select a directory')
        if len(tempdir) > 0:
            return tempdir

    def downloadFile(self, link, dir):
        root = tk.Tk()
        root.overrideredirect(1)
        root.withdraw()

        # Check if path selected exist
        if not os.path.exists(dir):
            messagebox.showwarning(title="Error",
                                   message="The selected path doesn't exist. Please select a correct one")
            return

        if link.find('/') == -1:
            return
        name_file = os.path.basename(link)
        extension = name_file.split['.'][-1]

        # Check if file has an extension
        if len(extension) < 1:
            messagebox.showwarning(title="Error",
                                   message="The link hasn't an extension.")
            return

        # Check if file already exist in the folder
        if os.path.isfile(dir + '/' + name_file):
            messagebox.showwarning(title="Error",
                                   message="The file already exist in the folder.")
            return

        # self.controller.createDownloadItemView()
        r = requests.get(link, stream=True)
        downloaded_file = open(dir + '/' + name_file, "wb")



        self.downloads.append(dir + '/' + name_file)
        self.activeDownloads.append(dir + '/' + name_file)
        for chunk in r.iter_content(chunk_size=256):
            if chunk:
                downloaded_file.write(chunk)
        self.activeDownloads.remove(dir + '/' + name_file)

