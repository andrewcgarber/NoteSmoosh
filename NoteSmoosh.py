# import the library

import PyPDF2
import pptx
import textract
import time
from appJar import gui
import shutil
from pathlib import Path
import tempfile
import os
from hyperlink import URL


# handle button events

def press1(button):
    if button == "File 1":
        filename1 = app.openBox(title="File 1", dirName="~/Documents", fileTypes=None, asFile=False, parent=None,
                                multiple=False, mode='r')
        app.label("File1", filename1, anchor='w', row=4, col=0)

    if button == "File 2":
        filename2 = app.openBox(title="File 2", dirName="~/Documents", fileTypes=None, asFile=False, parent=None,
                                multiple=False, mode='r')
        app.label("File2", filename2, anchor='w', row=5, col=0)

    if button == "Merge Notes!":

        filename1 = app.getLabel("File1")
        filename2 = app.getLabel("File2")
        app.okBox("Merge",
                  "Merging: \n\n" + filename1 + "\n\n                          and         \n\n" + filename2 + "\n",
                  parent=None)

        newfile = app.saveBox("New File Save")

        app.infoBox("Confirmed", "The merged content of the 2 files will be in  " + newfile)

        if (Path(filename1).suffix.upper() == ".PDF" or Path(filename1).suffix.upper() == ".DOCX" or \
            Path(filename1).suffix.upper() == ".TXT" or Path(filename1).suffix.upper() == ".PPTX") and \
            (Path(filename2).suffix.upper() == ".PDF" or Path(filename2).suffix.upper() == ".DOCX" or \
             Path(filename2).suffix.upper() == ".TXT" or Path(filename2).suffix.upper() == ".PPTX"):
            text1 = textract.process(filename1)
            text2 = textract.process(filename2)
            dirname, basename = os.path.split(filename1)
            dirname2, basename2 = os.path.split(filename2)
            temp1 = tempfile.NamedTemporaryFile(prefix=basename, dir=dirname)
            temp2 = tempfile.NamedTemporaryFile(prefix=basename2, dir=dirname2)
            temp1.write(text1)
            temp2.write(text2)
            
            with open(newfile, "wb") as wfd:
                for f in [temp1.name, temp2.name]:
                    with open(f, "rb") as fd:
                        shutil.copyfileobj(fd, wfd, 1024 * 1024 * 10)
            app.infoBox("Success", "Merge is successful!")
            app.yesNoBox("Y/N", "Do you want to view it?")

            temp1.close()
            temp2.close()

            if button == "No":
                app.label("File1", "File 1 Source: ", anchor='w', row=4, col=0)
                app.label("File2", "File 2 Source: ", anchor='w', row=5, col=0)
                exit()

            else:
                print()
                c = open(newfile, "r")
                app.infoBox("Combined Text", c.read())
                c.close()
                app.label("File1", "File 1 Source: ", anchor='w', row=4, col=0)
                app.label("File2", "File 2 Source: ", anchor='w', row=5, col=0)

        else:
                app.infoBox("Error", "Invalid File! This tool accepts PDF, DOCX, TXT, and PPTX only.")
                app.label("File1", "File 1 Source: ", anchor='w', row=4, col=0)
                app.label("File2", "File 2 Source: ", anchor='w', row=5, col=0)

def press3():
    filename = app.openBox(title=None, dirName="~/Documents", fileTypes=None, asFile=False, parent=None, multiple=False, mode='r')
    app.label("File3", filename, anchor='w', row=11, col=0)



def press4():
    filename = app.getLabel("File3")
    app.infoBox("Convert", "Are you sure you want to convert\n" + filename + "?", parent=None)
    newfile = app.saveBox("New File Save")
    app.infoBox("Processing", "Processing. This may take up to 30 seconds.")
    text = textract.process(filename)
    #print(text)
    str(text, 'utf-8')
    print (str(text, 'utf-8'))
    with open(newfile, "wb") as f:
        f.write(text)
    app.infoBox("Success", "Decode is successful! \n It is saved in:" + newfile)
    app.label("File3", "File Source: " + filename3, anchor='w', row=11, col=0)


def run():
    # start the GUI
    app.go()

def menuBar(btn):
    if btn == "Exit":
        exit()
    if btn == "Help":
        url = URL.from_text(u'http://github.com/python-hyper/hyperlink?utm_source=readthedocs')
        print(url)
        app.infoBox("Help", "Please refer to the User's Manual located at this URL:" + url.to_text())
    if btn == "About":
        app.infoBox("About", "About")
# function to update status bar with the time

def showTime():
    app.setStatusbar(time.strftime("%X"))

# create a GUI
app = gui("NoteSmoosh", "450x400")
app.setBg("white")
app.setFont(12)

# Add menu items
app.addMenuItem("File", "Exit", menuBar)
app.addMenuItem("Help", "Help", menuBar)
app.addMenuItem("About", "About", menuBar)
# add a statusbar to show the time
app.addStatusbar(side="RIGHT")
app.registerEvent(showTime)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to NoteSmoosh")
app.setLabelBg("title", "blue")
app.setLabelFg("title", "yellow")

app.addHorizontalSeparator(1, 0, 2, colour="red")

app.addLabel("l1", "Merge Tool")
app.setLabelBg("l1", "blue")
app.setLabelFg("l1", "yellow")

# link the buttons to the function called press
app.addButtons(["File 1", "File 2"], press1)
filename1 = ""
filename2 = ""
app.label("File1", "File 1 Source: " + filename1, anchor='w', row=4, col=0)
app.label("File2", "File 2 Source: " + filename2, anchor='w', row=5, col=0)
app.addLabel("Warn1", "*ONLY ACCEPTS PDF, DOCX, TXT")
app.addLabel("Warn2", "AND PPT FILES*")
app.setLabelFg("Warn1", "red")
app.setLabelFg("Warn2", "red")
app.addButtons(["Merge Notes!"], press1)

app.addLabel("l3", "Image Conversion Tool")
app.setLabelBg("l3", "blue")
app.setLabelFg("l3", "yellow")

app.addButtons(["File"], press3)
filename3 = ""
app.label("File3", "File Source: " + filename3, anchor='w', row=11, col=0)
app.addLabel("l4", "*ONLY ACCEPTS IMAGE FILES*")
app.setLabelFg("l4", "red")
app.addButtons(["Digitize!"], press4)

