# Download Manager
This application allows the user to download files of any format and manage many aspects of it.


## Prerequisites
Package | Version
------- | -------
[Python](https://www.python.org) | 3.8
[PyQt](https://www.riverbankcomputing.com/software/pyqt/download5) | 5.9.2
[Tk](https://www.tcl.tk/software/tcltk/8.6.html) | 8.6.10
[requests](https://pypi.org/project/requests/) | 2.27.1
[sip](https://pypi.org/project/sip/4.19.8/) | 4.19.8

Even pickle, threading, math, datetime, uuid, time and sys modules are required for the execution of the application but are already available if you use Python 3.8.


## Usage
Just launch **main.py** with python (if you have a virtual environment, remember to activate it).
```bash
$ python3 main.py
```
The MainWindow presents itself like this: <br/>
![MainWindow.png](https://github.com/EdoardoBonanni/Download-Manager/blob/main/downloads/use-case%20MainWindow.png)

To open the Qdialog containing the history of all downloads go to "File" -> "History" or use the shortcut Ctrl+H. <br/>
![QDialog.png](https://github.com/EdoardoBonanni/Download-Manager/blob/main/downloads/use-case%20QDialog.png)


## Implementation
This application was created to practice on Model-View-Control design pattern and it's a part of Human Computer Interaction exam at Unifi - Florence.

### Overview
This application is composed by a MainWindow and a QDialog.
The MainWindow allows you to choose the storage location, start the download after choosing the storage path and the file to download and manage the possible operations on each download (Pause, Resume, Interrupt, Restart and Remove).   
The Qdialog maintains a persistent history of downloads that lists all completed/aborted downloads the user has executed, with statistics on time started and completed.

### Download
The download is implemented in **fileDownload.py**. 
This application is based on asynchronous programming, since the Download Manager must be capable of managing multiple downloads in a session.
This class defines every single download that is managed independently by the others. 
These objects can be created starting a download of a file or executing the restart of a previously stopped download.

### Models
**Model_MainWindow.py** defines the model relating to the signalControllerMainWindow which contains a list of downloads started, paused, interrupted or completed and a list of controllers of previous downloads.
**Model_downloadItem.py** is the model of downloadItemController. It has to track all the information necessary to manage a download (including the unique ID of the download, filename, bytes reads, total bytes, information on the status of the download and a reference to the controllers that manage this element). <br/>
**Model_history.py** defines the model relating to the signalControllerHistory which contains list of items of table (downloads started, completed and interrupted), a list that keep the status of downloads and a list of end_times of all downloads (used for determine if download is started but not completed). <br/>

### Views
**MainWindow.py** defines the view relating to the MainWindow which is composed of a menubar and the necessary elements to choose the storage location and start a download, moreover there is a ScrollArea where the widgets related to the downloads will be added. <br/>
**downloadItemView.py** is a QWidget that shows the informations and progress of the download and provides the user the possibility, thanks to its controller, of changing the status of it by clicking on the following buttons: Pause, Resume, Interrupt, Restart and Remove. <br/>
**historyView.py** defines the view that contains the list of all completed/aborted downloads that the user has executed and the related statistics.  

### Controllers
To manage downloads updates on the view I used the signals (supplied in qtcore.pyqtsignal) which are asynchronous threads that allow you to send messages containing status updates of the downloads. These messages will be sent to the controllers that will process the received information and update the views. <br/>
I created 2 controllers with a different purpose for the MainWindow: 
    
1. **controllerMainWindow.py** manages operations that can be made by the user on the static components of the view i.e. choose the storage location, start a download, open the list of all completed/aborted downloads and close the window; <br/>
2. **signalControllerMainWindow.py** which updates the elements in the ScrollArea with the infomations/messages received through the signals that notify downloads updates. <br/>

**downloadItemController.py** manages operations that can be performed by the user on each download i.e. Pause, Resume, Interrupt, Restart and Remove. Obviously when the user makes one of these operations, a signal will be sent to the SignalcontrollerWindow that will update the elements in the ScrollArea. <br/>
**signalControllerHistory.py** updates the elements in the TableView with the infomations/messages received through the signals that notify downloads updates. Since the Tableview is not changeable, a controller that manages user operations on this widget is not necessary.  



