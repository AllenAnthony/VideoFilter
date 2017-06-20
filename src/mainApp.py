#!/usr/bin/env python

__author__ = 'Chenghao Jia & Xufeng Qian'

from Tkinter import *
import ttk
from videoFilters import Video
from tkFileDialog import askopenfilename
import cv2

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.onExit)

        self.videothread = Video()
        self.videothread.setFile('')
        # self.videothread.setFile(0)
        self.videothread.start()

        BUTTONWIDTH = 15
        SPINBOXWIDTH = 6
########################################################
        frame = Frame(self.root, padx=5)
        frame.grid(row=0,column=0, rowspan=2)
        
        self.butpick = Button(frame, text="Open File", fg='#991111', width=BUTTONWIDTH, command=self.pick)
        self.butpick.pack(side=TOP)
        self.butwebcam = Button(frame, text='Camera', fg='#991111', width=BUTTONWIDTH, command=self.webcam)
        self.butwebcam.pack(side=TOP)

########################################################
        Frame(self.root)
########################################################
        
        frame = Frame(self.root)
        frame.grid(row=0, column=1,columnspan=4,rowspan=2)
        

        self.filestr = StringVar()
        self.filestr.set("Open a video file or open your camera.")
        self.labfile = Label(frame, textvariable=self.filestr)
        self.labfile.pack(pady = 4)

        self.butplay = Button(frame, text="Play", fg = '#116611', width=BUTTONWIDTH, command=self.run)
        self.butplay.pack(side=LEFT, padx = 5)

        self.butstop = Button(frame, text="Stop", fg = '#116611', width=BUTTONWIDTH, command=self.stop)
        self.butstop.pack(side=LEFT, padx = 5)

        self.butrew = Button(frame, text="Rewind", fg = '#116611', width=BUTTONWIDTH, command=self.rewind)
        self.butrew.pack(side=LEFT, padx = 5)
#######################################################
        Frame(self.root, height=10).grid(row=4, column=0, columnspan=3)
#######################################################
        self.butfilgrayscale = Button(self.root, text="Grayscale", fg = '#111166', width=BUTTONWIDTH, command=self.grayscale)
        self.butfilgrayscale.grid(row=5, column=0)

        self.butfilinvert = Button(self.root, text="Invert", fg = '#111166', width=BUTTONWIDTH, command=self.invert)
        self.butfilinvert.grid(row=5, column=1)

        self.butfilhisteql = Button(self.root, text="Histogram equal", fg = '#111166', width=BUTTONWIDTH, command=self.histeql)
        self.butfilhisteql.grid(row=5, column=2)

        self.butfiledges = Button(self.root, text="Edges", fg = '#111166', width=BUTTONWIDTH, command=self.edges)
        self.butfiledges.grid(row=5, column=3)

        self.butcardColor = Button(self.root, text="CardColor", fg='#111166', width=BUTTONWIDTH, command=self.card)
        self.butcardColor.grid(row=6,column=0)

##        self.butdiff = Button(self.root, text="Diff", fg='#111166', width=BUTTONWIDTH, command=self.diff)
##        self.butdiff.grid(row=6, column=1)

        self.butgaussian = Button(self.root, text="Gaussian Blur", fg='#111166', width=BUTTONWIDTH, command=self.gaussian)
        self.butgaussian.grid(row=15, column=0)
        frame = Frame(self.root)
        frame.grid(row=15, column=1, columnspan=4, sticky=W, padx=20)
        self.spingaussianblurx = Spinbox(frame, from_=3, to=17, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.gaussianblurspin)
        self.spingaussianblurx.pack(side=LEFT)
        Label(frame, text="width of kernel").pack(side=LEFT, ipadx=10)
        self.spingaussianblury = Spinbox(frame, from_=3, to=17, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.gaussianblurspin)
        self.spingaussianblury.pack(side=LEFT)
        Label(frame, text="height of kernel").pack(side=LEFT, ipadx=10)

        self.butmedianBlur = Button(self.root, text="Median Blur", fg='#111166', width=BUTTONWIDTH, command=self.medianBlur)
        self.butmedianBlur.grid(row=14, column=0)
        frame = Frame(self.root)
        frame.grid(row=14, column=1,columnspan=4,sticky=W, padx=20)
        self.spinmedianBlur=Spinbox(frame, from_=3, to=17, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.medianblurspin)
        self.spinmedianBlur.pack(side=LEFT)
        Label(frame, text="size of kernel").pack(side=LEFT, ipadx=10)

        self.butaverage = Button(self.root, text="Average Blur", fg='#111166', width=BUTTONWIDTH, command=self.average)
        self.butaverage.grid(row=16,column=0)
        frame = Frame(self.root)
        frame.grid(row=16,column=1,columnspan=4,sticky=W, padx=20)
        self.spinaverageblurx = Spinbox(frame, from_=2, to=20, increment=1, width=SPINBOXWIDTH, state="readonly", command=self.averageblurspin)
        self.spinaverageblurx.pack(side=LEFT)
        Label(frame, text="width of kernel").pack(side=LEFT, ipadx=10)
        self.spinaverageblury = Spinbox(frame, from_=2, to=20, increment=1, width=SPINBOXWIDTH, state="readonly", command=self.averageblurspin)
        self.spinaverageblury.pack(side=LEFT)
        Label(frame, text="height of kernel").pack(side=LEFT, ipadx=10)
    

        self.butnorm = Button(self.root, text="Normalize", fg='#111166', width=BUTTONWIDTH, command=self.normalize)
        self.butnorm.grid(row=6,column=1)

        self.butmap = Button(self.root, text="Map Color", fg='#111166', width=BUTTONWIDTH, command=self.mapColor)
        self.butmap.grid(row=7, column=0)
        frame = Frame(self.root)
        frame.grid(row=7,column=1, columnspan=4, sticky=W, padx=20)
        self.combomap = ttk.Combobox(frame)
        self.combomap["state"]="readonly"
        self.combomap.bind("<<ComboboxSelected>>", self.mapcombo)
        self.combomap['values'] = ("AUTUMN","BONE","JET","WINTER","RAINBOW","OCEAN","SUMMER","SPRING","COOL","HSV","PINK","HOT")
        self.combomap.current(0)
        self.combomap.pack(side=LEFT)
        
        self.butfilthresh = Button(self.root, text="Thresholding", fg = '#111166', width=BUTTONWIDTH, command=self.thresholding)
        self.butfilthresh.grid(row=8, column=0)
        frame = Frame(self.root)
        frame.grid(row=8, column=1,columnspan=4, sticky = W, padx=20)
        var = StringVar()
        var.set(125)
        self.spinfilthresh = Spinbox(frame, from_=0, to=255, increment=1, textvariable=var, width=SPINBOXWIDTH, state="readonly", command=self.thresholdingspin)
        self.spinfilthresh.pack(side=LEFT)
        Label(frame, text="threshold value").pack(side=LEFT, ipadx=10)

        self.butfilreducecolor = Button(self.root, text="Reduce colors", fg = '#111166', width=BUTTONWIDTH, command=self.reducecolors)
        self.butfilreducecolor.grid(row=9, column=0)
        frame = Frame(self.root)
        frame.grid(row=9, column=1,columnspan=4, sticky = W, padx=20)
        self.spinfilreducecolor = Spinbox(frame, from_=2, to=255, increment=1, width=SPINBOXWIDTH, state="readonly", command=self.reducecolorsspin)
        self.spinfilreducecolor.pack(side=LEFT)
        Label(frame, text="total levels on channel").pack(side=LEFT, ipadx=10)

##        self.butfilmedian = Button(self.root, text="Median", fg = '#111166', width=BUTTONWIDTH, command=self.median)
##        self.butfilmedian.grid(row=10, column=0)
##        frame = Frame(self.root)
##        frame.grid(row=10, column=1,columnspan=4, sticky = W, padx=20)
##        self.spinfilmedian = Spinbox(frame, from_=3, to=31, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.medianspin)
##        self.spinfilmedian.pack(side=LEFT)
##        Label(frame, text="size of the window").pack(side=LEFT, ipadx=10)
##
##        self.butfilblur = Button(self.root, text="Blur", fg = '#111166', width=BUTTONWIDTH, command=self.blur)
##        self.butfilblur.grid(row=11, column=0)
##        frame = Frame(self.root)
##        frame.grid(row=11, column=1,columnspan=4, sticky = W, padx=20)
##        self.spinfilblur = Spinbox(frame, from_=3, to=31, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.blurspin)
##        self.spinfilblur.pack(side=LEFT)
##        Label(frame, text="kernel size").pack(side=LEFT, ipadx=10)

        self.butfilsharp = Button(self.root, text="Sharpen", fg = '#111166', width=BUTTONWIDTH, command=self.sharpen)
        self.butfilsharp.grid(row=12, column=0)
        frame = Frame(self.root)
        frame.grid(row=12, column=1,columnspan=4, sticky = W, padx=20)
        self.spinfilsharp = Spinbox(frame, from_=3, to=31, increment=2, width=SPINBOXWIDTH, state="readonly", command=self.sharpenspin)
        self.spinfilsharp.pack(side=LEFT)
        Label(frame, text="kernel size").pack(side=LEFT, ipadx=10)

        

        self.butfilcanny = Button(self.root, text="Canny", fg = '#111166', width=BUTTONWIDTH, command=self.canny)
        self.butfilcanny.grid(row=13, column=0)
        frame = Frame(self.root)
        frame.grid(row=13, column=1, columnspan=4,sticky = W, padx=20)
        self.spinfilcanny = Spinbox(frame, from_=10, to=500, increment=10, width=SPINBOXWIDTH, state="readonly", command=self.cannyspin)
        self.spinfilcanny.pack(side=LEFT)
        Label(frame, text="threshold1").pack(side=LEFT, ipadx=10)
        self.spinfilcanny2 = Spinbox(frame, from_=50, to=500, increment=10, width=SPINBOXWIDTH, state="readonly", command=self.cannyspin)
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
        self.filestr.set("Camera")

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

    def medianblurspin(self):
        self.videothread.medianSize2 = int(self.spinmedianBlur.get())

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

    def card(self):
        self.videothread.cardColorFun = not self.videothread.cardColorFun
        if self.videothread.cardColorFun:
            self.butcardColor.config(relief=SUNKEN, bg = '#CCCCCC')
        else :
            self.butcardColor.config(relief=RAISED, bg = '#EEEEEE')

    def diff(self):
        self.videothread.diffFun = not self.videothread.diffFun
        if self.videothread.diffFun:
            self.butdiff.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butdiff.config(relief=RAISED, bg = '#EEEEEE')

    def gaussian(self):
        self.videothread.gaussianBlurFun = not self.videothread.gaussianBlurFun
        if self.videothread.gaussianBlurFun:
            self.butgaussian.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butgaussian.config(relief=RAISED, bg = '#EEEEEE')

    def medianBlur(self):
        self.videothread.medianBlurFun = not self.videothread.medianBlurFun
        if self.videothread.medianBlurFun:
            self.butmedianBlur.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butmedianBlur.config(relief=RAISED, bg = '#EEEEEE')

    def average(self):
        self.videothread.averageBlurFun = not self.videothread.averageBlurFun
        if self.videothread.averageBlurFun:
            self.butaverage.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butaverage.config(relief=RAISED, bg = '#EEEEEE')

    def normalize(self):
        self.videothread.normalizationFun = not self.videothread.normalizationFun
        if self.videothread.normalizationFun:
            self.butnorm.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butnorm.config(relief=RAISED, bg = '#EEEEEE')

    def mapColor(self):
        self.videothread.mapColorFun = not self.videothread.mapColorFun
        if self.videothread.mapColorFun:
            self.butmap.config(relief=SUNKEN, bg = '#CCCCCC')
        else:
            self.butmap.config(relief=RAISED, bg = '#EEEEEE')

    def mapcombo(self, value):
        colormap=self.combomap.get()
        if colormap=="AUTUMN":
            self.videothread.COLORMAP=cv2.COLORMAP_AUTUMN
        elif colormap=="BONE":
            self.videothread.COLORMAP=cv2.COLORMAP_BONE
        elif colormap=="JET":
            self.videothread.COLORMAP=cv2.COLORMAP_JET
        elif colormap=="WINTER":
            self.videothread.COLORMAP=cv2.COLORMAP_WINTER
        elif colormap=="RAINBOW":
            self.videothread.COLORMAP=cv2.COLORMAP_RAINBOW
        elif colormap=="OCEAN":
            self.videothread.COLORMAP=cv2.COLORMAP_OCEAN
        elif colormap=="SUMMER":
            self.videothread.COLORMAP=cv2.COLORMAP_SUMMER
        elif colormap=="SPRING":
            self.videothread.COLORMAP=cv2.COLORMAP_SPRING
        elif colormap=="COOL":
            self.videothread.COLORMAP=cv2.COLORMAP_COOL
        elif colormap=="HSV":
            self.videothread.COLORMAP=cv2.COLORMAP_HSV
        elif colormap=="PINK":
            self.videothread.COLORMAP=cv2.COLORMAP_PINK
        else:
            self.videothread.COLORMAP=cv2.COLORMAP_HOT

    def cannyspin(self):
        self.videothread.cannynumber = int(self.spinfilcanny.get())
        self.videothread.cannynumber2 = int(self.spinfilcanny2.get())

    def averageblurspin(self):
        self.videothread.averageX = int(self.spinaverageblurx.get())
        self.videothread.averageY = int(self.spinaverageblury.get())

    def gaussianblurspin(self):
        self.videothread.gaussianX = int(self.spingaussianblurx.get())
        self.videothread.gaussianY = int(self.spingaussianblury.get())

    def onExit(self):
        self.videothread.exit = True
        self.root.quit()

##############################################

if __name__ == "__main__":
    main = Tk()
    main.title("Control")
    app = VideoPlayer(main)
    main.mainloop()
