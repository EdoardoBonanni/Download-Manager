import tkinter as tk
from tkinter import filedialog, messagebox
import os, requests

def chooseDirectory(initialdir):
    root = tk.Tk()
    root.withdraw() #use to hide tkinter window

    tempdir = filedialog.askdirectory(parent=root, initialdir=initialdir, title='Please select a directory')
    if len(tempdir) > 0:
        return tempdir

def downloadFile(link, dir):
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    if link.find('/') == -1:
        return
    name_file = os.path.basename(link)

    # Check if path selected exist
    if not os.path.exists(dir):
        messagebox.showwarning(title="Error",
                               message="The selected path doesn't exist. Please select a correct one")
        return

    # Check if file already exist in the folder
    if os.path.isfile(dir + '/' + name_file):
        messagebox.showwarning(title="Error",
                               message="The file already exist in the folder.")
        return

    r = requests.get(link, stream=True)
    downloaded_file = open(dir + '/' + name_file, "wb")
    for chunk in r.iter_content(chunk_size=256):
        if chunk:
            downloaded_file.write(chunk)


