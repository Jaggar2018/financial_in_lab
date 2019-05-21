import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from PIL import Image
from skimage.morphology import disk
import skimage.filters.rank as sfr
from skimage import data,color


def histogram_demo(image):
    plt.hist(image.ravel(), 256, [0, 256])#ravel函数功能是将多维数组降为一维数组
    plt.show()

image1 = cv.imread('C:/Users/Jagga/Desktop/DIP/im/13.bmp', 1)
image2 = cv.imread('C:/Users/Jagga/Desktop/DIP/im/14.bmp', 1)
image3 = cv.imread('C:/Users/Jagga/Desktop/DIP/im/15.bmp', 1)
image4 = cv.imread('C:/Users/Jagga/Desktop/DIP/im/16.bmp', 1)
cv.imshow('souce image', image)
histogram_demo(image1)
histogram_demo(image2)
histogram_demo(image3)
histogram_demo(image4)
cv.waitKey(0)
cv.destroyAllWindows()
mb=cv.medianBlur(image2,3)
mj=cv.blur(image2,(3,3))
mg=cv.GaussianBlur(image2,(3,3),0)
cv.imshow('median',mb)
cv.imshow('aver',mj)
cv.imshow('gaussion',mg)

std_image = tf.image.per_image_standardization(image4)
with tf.Session() as sess:
    result = sess.run(std_image)
    print(result)
    cv.imshow('nor',result)
cv.waitKey()
cv.destroyAllWindows()

############### picture 13 ################

mb=cv.medianBlur(image1,5)
cv.imshow('median',mb)
std_image = tf.image.per_image_standardization(mb)

with tf.Session() as sess:
    result = sess.run(std_image)
    cv.imshow('result',result)

kernel= np.ones((3,3),np.uint8)
pening = cv.morphologyEx(result, cv.MORPH_OPEN, kernel)
cv.imshow('pening',pening)
kernel2= np.ones((3,3),np.uint8)
closing = cv.morphologyEx(result, cv.MORPH_CLOSE, kernel2)

cv.imshow('closing',closing)
cv.waitKey()
cv.destroyAllWindows()

################ picture 14 ################

mb=cv.medianBlur(image2,5)
mg=cv.GaussianBlur(mb,(3,3),0)
cv.imshow('median',mb)
cv.imshow('gaussion',mg)
std_image = tf.image.per_image_standardization(mb)
std_image2 = tf.image.per_image_standardization(mg)
with tf.Session() as sess:
    result = sess.run(std_image)
    cv.imshow('result',result)
    result2 = sess.run(std_image2)
    cv.imshow('result2', result2)

kernel= np.ones((3,3),np.uint8)
pening = cv.morphologyEx(result, cv.MORPH_OPEN, kernel)
cv.imshow('pening',pening)
kernel2= np.ones((3,3),np.uint8)
closing = cv.morphologyEx(pening, cv.MORPH_CLOSE, kernel2)

cv.imshow('closing',closing)
cv.waitKey()
cv.destroyAllWindows()

cv.waitKey()
cv.destroyAllWindows()

################ picture 14 ################

mb=cv.blur(image3,(5,5))

cv.imshow('median',mb)

std_image = tf.image.per_image_standardization(mb)

with tf.Session() as sess:
    result = sess.run(std_image)
    cv.imshow('result',result)

kernel = np.ones((3,3),np.uint8)
erosion = cv.erode(result,kernel,iterations = 1)
dilation = cv.dilate(erosion,kernel,iterations = 1)
cv.imshow('erosion',erosion)
cv.imshow('dilation',dilation)

cv.waitKey()
cv.destroyAllWindows()

################# picture 15 ################

mb=cv.blur(image4,(5,5))

cv.imshow('median',mb)

std_image = tf.image.per_image_standardization(mb)

with tf.Session() as sess:
    result = sess.run(std_image)
    cv.imshow('result',result)


kernel2= np.ones((5,5),np.uint8)
closing = cv.morphologyEx(result, cv.MORPH_CLOSE, kernel2)

cv.imshow('closing',closing)
histogram_demo(closing)
cv.waitKey()
cv.destroyAllWindows()

