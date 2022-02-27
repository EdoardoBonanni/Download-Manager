import math
import tkinter as tk
from tkinter import filedialog

def convert_size(size_bytes):
    # Converts the number of bytes in a measure more easily readable by the user
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def chooseDirectory(initialdir):
    # use tkinter for select the download directory to the user
    root = tk.Tk()
    root.withdraw() # use to hide tkinter window

    tempdir = filedialog.askdirectory(parent=root, initialdir=initialdir, title='Please select a directory')
    if len(tempdir) > 0:
        return tempdir
    else:
        return initialdir