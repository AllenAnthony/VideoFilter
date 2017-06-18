import threading
import numpy as np
import cv2
import copy
import datetime
from scipy.misc import imread

# A = y/4 + (x/32)*64
# B = z/4 + ((x%32)/4)*64

def myFilter(img, change):
    for i in xrange(len(img)):
        for j in xrange(len(img[0])):
            pos = [img[i][j][1]/4+(img[i][j][0]/32)*64,img[i][j][2]/4 + ((img[i][j][0]%32)/4)*64]
            img[i][j] = change[pos[0], pos[1]]

def filter(img):
    dstImage = copy.deepcopy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.multiply(cv2.add(img, -minVal), 255 / (maxVal - minVal),dstImage)  # Calculates the per-element scaled product of two arrays.
    return dstImage

def ave(img):
    frame=copy.deepcopy(img)
    X=9
    Y=9
    kernel = np.ones((X, Y), np.float32) / (X * Y)
    return cv2.filter2D(frame, -1, kernel)

def medianBlur(img,size):# medianBlur with size*size
    return cv2.medianBlur(img,size)

# blurkernel=[]
# sharpenkernel=[]
#
# for i in range(3,32,2):
#     blurkernel.insert(i/2-1, cv2.getGaussianKernel(i,0) * cv2.transpose(cv2.getGaussianKernel(i,0)))
#
# for i in range(3,32,2):
#      sharpenkernel.insert(i/2-1,blurkernel[i/2-1].copy())
#      sharpenkernel[i/2-1][i/2][i/2] -= 1.8
#      sharpenkernel[i/2-1] *=- 1
# sharpenkernelsize = 3
#
# edgeskernel = np.array([[-1.,  -1.,  -1.],
#                         [-1.,   8.,  -1.],
#                         [-1.,  -1.,  -1.]])

filename= "./111.jpg"
img = cv2.imread(filename)
# print len(img)
# print len(img[0])
# print img[0][0]
#change = cv2.imread("./change.png")
#frame = cv2.filter2D(img, -1, sharpenkernel[sharpenkernelsize / 2 - 1])
# changeImg=copy.deepcopy(img)
# before = datetime.datetime.now()
# myFilter(changeImg,change)
# after = datetime.datetime.now()
# delta = after - before
# print delta
#img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#frame = medianBlur(img,8)

if img.size>0:
    cv2.imshow('before',img)
    #cv2.imshow("filter",frame)
    cv2.imshow("filter",medianBlur(img,9))

cv2.waitKey(0)
cv2.destroyAllWindows()


# frame1 = cv2.medianBlur(img, 3)
# frame2 = cv2.Canny(img, 10, 30)
# frame3 = cv2.filter2D(img, -1, edgeskernel)

# reducechannelvalues=10
# frame = img.astype(np.float16)
# frame = (frame / (255./(reducechannelvalues-1))).round() * (255/(reducechannelvalues-1))
# frame = frame.astype(np.uint8)

# retval, frame = cv2.threshold(img,125,255,cv2.THRESH_BINARY)


# class Video(threading.Thread):
#     def __init__(self):
#         super(Video, self).__init__()
#
#         self.play = True
#         self.exit = False
#         self.waitPerFrameInMillisec = 1
#         self.filename = ''
#
#     # no.1
#         self.grayscale = False
#     # no.2
#         self.invert = False
#     # no.3
#         self.histeql = False
#     # no.4
#         self.thresholding = False
#         self.threshold = 125
#     # no.5
#         self.reducecolors = False
#         self.reducechannelvalues = 2
#     # no.5
#         self.median = False
#         self.mediansize = 3
#     # no.6
#         self.blur = False
#         self.blurkernelsize = 3
#         self.blurkernel = []
#     # no.7
#         self.sharpen = False
#         self.sharpenkernelsize = 3
#         self.sharpenkernel = []
#     # no.8
#         self.edges = False
#         self.edgeskernel = []
#     # no.9
#         self.canny = False
#         self.cannynumber = 10
#         self.cannynumber2 = 30
#
# ###############generate 15 blur kernels Gaussian from 3*3 to 31*31
#         for i in range(3,32,2):
#             self.blurkernel.insert(i/2-1, cv2.getGaussianKernel(i,0) * cv2.transpose(cv2.getGaussianKernel(i,0)))
#         #0-14:3-31
#         # print("Blur Kernel my")
#         # print(self.blurkernel)
#
#
# ###############generovani sharpen kernelu
#         # for i in range(3,32,2):
#         #     self.sharpenkernel.insert(i, cv2.Laplacian(self.blurkernel[i/2-1], cv2.CV_64F))
#         #     self.sharpenkernel[i/2-1] *= -1
#         for i in range(3,32,2):
#             self.sharpenkernel.insert(i,self.blurkernel[i/2-1].copy())
#             self.sharpenkernel[i/2-1][i/2][i/2] -= 2.
#             self.sharpenkernel[i/2-1] *=- 1
#
#         mylist=[]
#         for i in range(3,32,2):
#             mylist.insert(i/2-1,self.blurkernel[i/2-1].copy())
#             mylist[i/2-1][i/2][i/2] -= 2.
#             mylist[i/2-1] *=- 1
#
#         print mylist[0]
#         print "\n",self.sharpenkernel[0]
#         print "\n",self.blurkernel[0]
#
# test=Video()
# print 0==''



