#!/usr/bin/env python
__author__ = 'Jakub Kvita & Jan Bednarik'

from Tkinter import *
from videoFilters import Video
from tkFileDialog import askopenfilename
import cv2

class VideoPlayer:
    def __init__(self, root):# root is a windows
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.onExit)

        self.videothread = Video()
        self.videothread.setFile('')
        # self.videothread.setFile(0)
        self.videothread.start()

        BUTTONWIDTH = 15
        SPINBOXWIDTH = 6
########################################################
        self.butpick = Button(self.root, text="Pick file", fg = '#991111', width=BUTTONWIDTH, command=self.pick)
        self.butpick.grid(row=0, column=0)

        self.filestr = StringVar()
        self.filestr.set("")
        self.labfile = Label(self.root, textvariable=self.filestr)
        self.labfile.grid(row=0, column=1, columnspan=5, rowspan=2)

        self.butwebcam = Button(self.root, text="Webcam", fg = '#991111', width=BUTTONWIDTH, command=self.webcam)
        self.butwebcam.grid(row=1, column=0)
########################################################
        Frame(self.root, height=10).grid(row=2, column=0, columnspan=3)
########################################################
        self.butplay = Button(self.root, text="Play", fg = '#116611', width=BUTTONWIDTH, command=self.run)
        self.butplay.grid(row=3, column=0)

        frame = Frame(self.root)
        frame.grid(row=3, column=1,columnspan=2, sticky = W)

        self.butstop = Button(frame, text="Stop", fg = '#116611', width=BUTTONWIDTH, command=self.stop)
        self.butstop.pack(side=LEFT)

        self.butrew = Button(frame, text="Rewind", fg = '#116611', width=BUTTONWIDTH, command=self.rewind)
        self.butrew.pack(side=LEFT)
#######################################################
        Frame(self.root, height=10).grid(row=4, column=0, columnspan=3)
#######################################################
        self.butfilgrayscale = Button(self.root, text="Grayscale", fg = '#111166', width=BUTTONWIDTH, command=self.grayscale)
        self.butfilgrayscale.grid(row=5, column=0)

        self.butfilinvert = Button(self.root, text="Invert", fg = '#111166', width=BUTTONWIDTH, command=self.invert)
        self.butfilinvert.grid(row=6, column=0)

        self.butfilhisteql = Button(self.root, text="Histogram equal.", fg = '#111166', width=BUTTONWIDTH, command=self.histeql)
        self.butfilhisteql.grid(row=7, column=0)

        self.butfilthresh = Button(self.root, text="Thresholding", fg = '#111166', width=BUTTONWIDTH, command=self.thresholding)
        self.butfilthresh.grid(row=8, column=0)
        frame = Frame(self.root)
        frame.grid(row=8, column=1,columnspan=2, sticky = W, padx=20)
        var = StringVar()
        var.set(125)
        self.spinfilthresh = Spinbox(frame, from_=0, to=255, increment=1, textvariable=var, width=SPINBOXWIDTH, state="readonly", command=self.thresholdingspin)
        self.spinfilthresh.pack(side=LEFT)
        Label(frame, text="threshold value").pack(side=LEFT, ipadx=10)

        self.butfilreducecolor = Button(self.root, text="Reduce colors", fg = '#111166', width=BUTTONWIDTH, command=self.reducecolors)
        self.butfilreducecolor.grid(row=9, column=0)
        frame = Frame(self.root)
        frame.grid(row=9, column=1,columnspan=2, sticky = W, padx=20)
        self.spinfilreducecolor = Spinbox(frame, from_=2, to=255, increment=1, width=SPINBOXWIDTH, state="readonly", command=self.reducecolorsspin)
        self.spinfilreducecolor.pack(side=LEFT)
        Label(frame, text="total levels on channel").pack(side=LEFT, ipadx=10)

        self.butfilmedian = Button(self.root, text="Median", fg = '#111166', width=BUTTONWIDTH, command=self.median)
        self.butfilmedian.grid(row=10, column=0)
        frame = Frame(self.root)
        frame.grid(row=10, column=1,columnspan=2, sticky = W, padx=20)
        self.spinfilmedian = Spinbox(frame, from_=3, to=31, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.medianspin)
        self.spinfilmedian.pack(side=LEFT)
        Label(frame, text="size of the window").pack(side=LEFT, ipadx=10)

        self.butfilblur = Button(self.root, text="Blur", fg = '#111166', width=BUTTONWIDTH, command=self.blur)
        self.butfilblur.grid(row=11, column=0)
        frame = Frame(self.root)
        frame.grid(row=11, column=1,columnspan=2, sticky = W, padx=20)
        self.spinfilblur = Spinbox(frame, from_=3, to=31, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.blurspin)
        self.spinfilblur.pack(side=LEFT)
        Label(frame, text="kernel size").pack(side=LEFT, ipadx=10)

        self.butfilsharp = Button(self.root, text="Sharpen", fg = '#111166', width=BUTTONWIDTH, command=self.sharpen)
        self.butfilsharp.grid(row=12, column=0)
        frame = Frame(self.root)
        frame.grid(row=12, column=1,columnspan=2, sticky = W, padx=20)
        self.spinfilsharp = Spinbox(frame, from_=3, to=31, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.sharpenspin)
        self.spinfilsharp.pack(side=LEFT)
        Label(frame, text="kernel size").pack(side=LEFT, ipadx=10)

        self.butfiledges = Button(self.root, text="Edges", fg = '#111166', width=BUTTONWIDTH, command=self.edges)
        self.butfiledges.grid(row=13, column=0)

        self.butfilcanny = Button(self.root, text="Canny", fg = '#111166', width=BUTTONWIDTH, command=self.canny)
        self.butfilcanny.grid(row=14, column=0)
        frame = Frame(self.root)
        frame.grid(row=14, column=1, columnspan=2,sticky = W, padx=20)
        self.spinfilcanny = Spinbox(frame, from_=10, to=500, increment=10, width=SPINBOXWIDTH, state="readonly", command=self.cannyspin)
        self.spinfilcanny.pack(side=LEFT)
        Label(frame, text="threshold1").pack(side=LEFT, ipadx=10)
        self.spinfilcanny2 = Spinbox(frame, from_=10, to=500, increment=10, width=SPINBOXWIDTH, state="readonly", command=self.cannyspin)
        self.spinfilcanny2.pack(side=LEFT)
        Label(frame, text="threshold2").pack(side=LEFT, ipadx=10)
######################################################
######################################################
    def pick(self):
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        if filename:
            self.filestr.set(filename)
            self.videothread.setFile(filename)

    def webcam(self):
        self.videothread.setFile(0)
        self.filestr.set("WEBCAM")

    def run(self):
        self.videothread.play = True

    def stop(self):
        self.videothread.play = False

    def rewind(self):
        self.videothread.setFile(self.videothread.filename)

    def grayscale(self):
        self.videothread.grayscale = not self.videothread.grayscale
        if self.videothread.grayscale:
            self.butfilgrayscale.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilgrayscale.config(relief=RAISED, bg = '#EEEEEE')

    def invert(self):
        self.videothread.invert = not self.videothread.invert
        if self.videothread.invert:
            self.butfilinvert.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilinvert.config(relief=RAISED, bg = '#EEEEEE')

    def histeql(self):
        self.videothread.histeql = not self.videothread.histeql
        if self.videothread.histeql:
            self.butfilhisteql.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilhisteql.config(relief=RAISED, bg = '#EEEEEE')

    def thresholding(self):
        self.videothread.thresholding = not self.videothread.thresholding
        if self.videothread.thresholding:
            self.butfilthresh.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilthresh.config(relief=RAISED, bg = '#EEEEEE')

    def thresholdingspin(self):
        self.videothread.threshold = int(self.spinfilthresh.get())

    def reducecolors(self):
        self.videothread.reducecolors = not self.videothread.reducecolors
        if self.videothread.reducecolors:
            self.butfilreducecolor.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilreducecolor.config(relief=RAISED, bg = '#EEEEEE')

    def reducecolorsspin(self):
        self.videothread.reducechannelvalues = int(self.spinfilreducecolor.get())

    def median(self):
        self.videothread.median = not self.videothread.median
        if self.videothread.median:
            self.butfilmedian.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilmedian.config(relief=RAISED, bg = '#EEEEEE')

    def medianspin(self):
        self.videothread.mediansize = int(self.spinfilmedian.get())

    def blur(self):
        self.videothread.blur = not self.videothread.blur
        if self.videothread.blur:
            self.butfilblur.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilblur.config(relief=RAISED, bg = '#EEEEEE')

    def blurspin(self):
        self.videothread.blurkernelsize = int(self.spinfilblur.get())

    def sharpen(self):
        self.videothread.sharpen = not self.videothread.sharpen
        if self.videothread.sharpen:
            self.butfilsharp.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilsharp.config(relief=RAISED, bg = '#EEEEEE')

    def sharpenspin(self):
        self.videothread.sharpenkernelsize = int(self.spinfilsharp.get())

    def edges(self):
        self.videothread.edges = not self.videothread.edges
        if self.videothread.edges:
            self.butfiledges.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfiledges.config(relief=RAISED, bg = '#EEEEEE')

    def canny(self):
        self.videothread.canny = not self.videothread.canny
        if self.videothread.canny:
            self.butfilcanny.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butfilcanny.config(relief=RAISED, bg = '#EEEEEE')

    def cannyspin(self):
        self.videothread.cannynumber = int(self.spinfilcanny.get())
        self.videothread.cannynumber2 = int(self.spinfilcanny2.get())

    def onExit(self):
        self.videothread.exit = True
        self.root.quit()

##############################################

if __name__ == "__main__":
    main = Tk()
    main.title("Control")
    app = VideoPlayer(main)
    main.mainloop()