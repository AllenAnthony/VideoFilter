#!/usr/bin/env python
#! coding:utf-8
__author__ = "Xufeng Qian & Chenghao Jia"

import threading
import numpy as np
import cv2
import cv2.cv as cv
import copy
import datetime

# cv2.filter2D(frame, -1, kernel) 用kernel这一个卷积核对frame的各个channel做处理

# YCbCr
# YCbCr其中Y是指亮度分量，Cb指蓝色色度分量，而Cr指红色色度分量
# Gray = R*0.299 + G*0.587 + B*0.114
# Gray = (R*30 + G*59 + B*11 + 50) / 100


def cardColor(img, changeCard):# the filter using the color card
    for i in xrange(len(img)):
        for j in xrange(len(img[0])):
            pos = [img[i][j][1]/4+(img[i][j][0]/32)*64,img[i][j][2]/4 + ((img[i][j][0]%32)/4)*64]
            img[i][j] = changeCard[pos[0], pos[1]]
    return img
# standard color card coordinate
# A = y/4 + (x/32)*64
# B = z/4 + ((x%32)/4)*64

def diff(img,diffImage):# the difference image between two images
    resImage = copy.deepcopy(img)
    cv2.absdiff(diffImage, img, resImage)#Calculates the per-element absolute difference between two arrays or between an array and a scalar.
    return resImage

def gaussianBlur(img,X,Y):# automatically GaussianBlur with size X*Y
    resImage = copy.deepcopy(img)
    return cv2.GaussianBlur(resImage, (X, Y), 0)

def medianBlur(img,size):# medianBlur with size*size
    resImage = copy.deepcopy(img)
    return cv2.medianBlur(resImage,size)

def averageBlur(img,X,Y):# averageBlur with size X*Y
    resImage=copy.deepcopy(img)
    kernel = np.ones((X, Y), np.float32) / (X * Y)
    return cv2.filter2D(resImage, -1, kernel)

def normalization(img):# 均匀化
    resImage = copy.deepcopy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

    channels = cv2.split(resImage)  # Divides a multi-channel array into several single-channel arrays.
    # Calculates the per-element scaled product of two arrays.
    cv2.multiply(cv2.add(channels[0], -minVal), 255 / (maxVal - minVal), channels[0])
    cv2.multiply(cv2.add(channels[1], -minVal), 255 / (maxVal - minVal), channels[1])
    cv2.multiply(cv2.add(channels[2], -minVal), 255 / (maxVal - minVal), channels[2])
    resImage = cv2.merge(channels)
    # cv2.multiply(cv2.add(img, -minVal), 255 / (maxVal - minVal),resImage)
    return resImage

def mapColor(img,COLORMAP):# color map: resImage = cv2.applyColorMap(img, cv2.COLORMAP_PINK)
    resImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resImage = cv2.applyColorMap(resImage, COLORMAP)
    return resImage

class Video(threading.Thread):
    def __init__(self):
        super(Video, self).__init__()

        self.play = True
        self.exit = False
        self.msecPerFrame = 1
        self.filename = ""

    # no.1
        self.grayscale = False
    # no.2
        self.invert = False
    # no.3
        self.histeql = False
    # no.4
        self.thresholding = False
        self.threshold = 125
    # no.5
        self.reducecolors = False
        self.reducechannelvalues = 2
    # no.5
        self.median = False
        self.mediansize = 3
    # no.6
        self.blur = False
        self.blurkernelsize = 3
        self.blurkernel = []
    # no.7
        self.sharpen = False
        self.sharpenkernelsize = 3
        self.sharpenkernel = []
    # no.8
        self.edges = False
        self.edgeKernel = []
    # no.9
        self.canny = False
        self.cannynumber = 10
        self.cannynumber2 = 30
    # no.10
        self.cardColorFun=False
        self.changeFileName="../change.png"
        self.changeCard=None
    # no.11
        self.diffFun = False
        self.diffFileName="../111.jpg"
        self.diffImage=None
    # no.12
        self.gaussianBlurFun=False
        self.gaussianX=9
        self.gaussianY=9
    # no.13
        self.medianBlurFun=False
        self.medianSize2=9
    # no.14
        self.averageBlurFun=False
        self.averageX=9
        self.averageY=9
    # no.15
        self.normalizationFun=False
    # no.16
        self.mapColorFun=False
        self.COLORMAP=cv2.COLORMAP_PINK





###############generate 15 Gaussian blur kernels from 3*3 to 31*31
        for i in range(3,32,2):
            self.blurkernel.insert(i/2-1, cv2.getGaussianKernel(i,0) * cv2.transpose(cv2.getGaussianKernel(i,0)))
        #0-14:3-31
        # print("Blur Kernel my")
        # print(self.blurkernel)

###############generate sharpen kernel
        # for i in range(3,32,2):
        #     self.sharpenkernel.insert(i, cv2.Laplacian(self.blurkernel[i/2-1], cv2.CV_64F))
        #     self.sharpenkernel[i/2-1] *= -1
        for i in range(3,32,2):
            #self.sharpenkernel.insert(i,self.blurkernel[i/2-1].copy())
            self.sharpenkernel.insert(i/2-1,self.blurkernel[i/2-1].copy())
            self.sharpenkernel[i/2-1][i/2][i/2] -= 2.# the center of current matrix minus 2 x-2
            self.sharpenkernel[i/2-1] *=- 1# turn all the ele in the matrix to negative -x,2-x
        # print("Sharpen Kernel my")
        # print(self.sharpenkernel)

#######################generate edge kernel
        self.edgeKernel = np.array([[-1.,  -1.,  -1.],
                                     [-1.,   8.,  -1.],
                                     [-1.,  -1.,  -1.]])



    def setFile(self, filename):
        if filename == 0 and self.filename == 0:
            return
        self.filename = filename
        self.cap = cv2.VideoCapture(self.filename)# open the video
        self.fps = self.cap.get(cv.CV_CAP_PROP_FPS)# get() return corresponding property CV_CAP_PROP_FPS:Frame rate.
        self.msecPerFrame = int(1.0 / self.fps * 1000) if self.fps > 0 else 15
        self.changeCard=cv2.imread(self.changeFileName)
        self.diffImage=cv2.imread(self.diffFileName)
        # print 'Frame Rate = ', self.fps, ' frames per sec'
        # print 'Wait between frames = ', self.msecPerFrame, ' ms'
        self.play = True



    def run(self):
        frameorig = []
        while not self.exit:
            #activeFilter = 0
    ####
            before = datetime.datetime.now()
    ####
            if self.cap.isOpened():
                if self.play:
                    #pokud hrajeme dal nactu dalsi, jinak porad tocim ten stary
                    ret, frameorig = self.cap.read() # Grabs, decodes and returns the next video frame
                    if(ret): # ret = true if read succeed, false otherwise
                        frame = frameorig
                    else:
                        self.play=False
                        self.exit=1
                        break
                else:
                    frame = frameorig



                ############################################ filter
                if self.grayscale:# transfer to gray image
                    #activeFilter+=1
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)# Converts an image from one color space to another

                if self.invert:# transfer to the invert
                    #activeFilter+=1
                    frame = (255-frame)

                if self.histeql:# 直方图均衡化
                    #activeFilter+=1
                    if self.grayscale:
                        frame = cv2.equalizeHist(frame)# Equalizes the histogram of a grayscale image.
                    else: # only equalize the histogram of layer Y(jas)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)## convert color space from rgb to ycbcr
                        channels = cv2.split(frame)# Divides a multi-channel array into several single-channel arrays.
                        channels[0] = cv2.equalizeHist(channels[0])
                        frame = cv2.merge(channels)# Creates one multichannel array out of several single-channel ones
                        frame = cv2.cvtColor(frame, cv2.COLOR_YCR_CB2BGR)

                if self.thresholding:# turn >125 to =125, turn <=215 to 0, 8 colors left finally
                    #activeFilter+=1
                    retval, frame = cv2.threshold(frame,self.threshold,255,cv2.THRESH_BINARY)# Applies a fixed-level threshold to each array element.

                if self.reducecolors:# divide the value of each channel into reducechannelvalues parts
                    #activeFilter+=25
                    frame = frame.astype(np.float16)
                    frame = (frame / (255./(self.reducechannelvalues-1))).round() * (255/(self.reducechannelvalues-1))
                    frame = frame.astype(np.uint8)

                if self.median:# Blurs an image using the median filter. 中值模糊
                    #activeFilter+=self.mediansize*2
                    frame = cv2.medianBlur(frame,self.mediansize)
                # The function smoothes an image using the median filter with the ksize*ksize aperture.
                # Each channel of a multi-channel image is processed independently

                if self.blur:# 高斯模糊
                    #activeFilter+=self.blurkernelsize*2
                    frame = cv2.filter2D(frame, -1, self.blurkernel[self.blurkernelsize/2-1])
                    # The function smoothes an image using the median filter with the ksize*ksize aperture.
                    # Each channel of a multi-channel image is processed independently.In-place operation is supported.

                if self.sharpen:# 锐化
                    #activeFilter+=self.sharpenkernelsize*2
                    frame = cv2.filter2D(frame, -1, self.sharpenkernel[self.sharpenkernelsize/2-1])# Convolves an image with the kernel.

                if self.edges: # 一种朴素的边缘算法
                    #activeFilter+=1
                    frame = cv2.filter2D(frame, -1, self.edgeKernel)# the third parameter is the convolve kernel

                # 图像的边缘检测的原理是检测出图像中所有灰度值变化较大的点，
                # 而且这些点连接起来就构成了若干线条，这些线条就可以称为图像的边缘。
                # Finds edges in an image using the [Canny86] algorithm. look up in canny原理.txt
                if self.canny:
                    #activeFilter+=1
                    frame = cv2.Canny(frame, self.cannynumber, self.cannynumber2)

                if self.cardColorFun:#卡色映射
                    frame=cardColor(frame,self.changeCard)

                if self.diffFun :#两个图像之差
                    frame=diff(frame,self.diffImage)

                if self.gaussianBlurFun:#高斯模糊
                    frame=gaussianBlur(frame,self.gaussianX,self.gaussianY)

                if self.medianBlurFun:#中值模糊
                    frame=medianBlur(frame,self.medianSize2)

                if self.averageBlurFun: #平均模糊
                    frame=averageBlur(frame,self.averageX,self.averageY)

                if self.normalizationFun:# 归一化
                    frame=normalization(frame)

                if(self.mapColorFun):# 颜色映射
                    frame=mapColor(frame,self.COLORMAP)

                ##########################################

                cv2.imshow("Video", frame)# Displays an image in the specified window
                ####
                after = datetime.datetime.now()
                delta = after - before
                print delta,"   ",delta.microseconds/1000
                msec=delta.microseconds/1000
                ###
                wait = self.msecPerFrame-msec
                # print wait

                # Waits for a pressed key for milliseconds, go on after key event happen or go on after time out
                # It returns the code of the pressed key or -1 if no key was pressed before the specified time had elapsed.
                # Delay in milliseconds. 0 is the special value that means “forever”.
                cv2.waitKey(wait if wait>0 else 1)
                # cv2.waitKey(self.msecPerFrame-int(delta.microseconds/10000.))
                # cv2.waitKey(1)
            else:
                #jestli neni nic otevreno tak cekam az si neco vybere a pusti
                cv2.waitKey(200)

        self.cap.release()
        cv2.destroyAllWindows()
