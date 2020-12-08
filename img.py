import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

res = [0, 0, 0]


def image_hist(image):
    color = ('b', 'g', 'r')
    for i, color in enumerate(color):
        hist = cv.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color)
        plt.xlim([0, 256])
    plt.show()


src = cv.imread('img1.png')
cv.namedWindow('input_image', cv.WINDOW_NORMAL)
cv.imshow('input_image', src)


for i in src.ravel():
    if i % 3 == 0:
        res[0] += src.ravel()[i]
    elif i % 3 == 1:
        res[1] += src.ravel()[i]
    elif i % 3 == 2:
        res[2] += src.ravel()[i]

print(src)
print(src.ravel())
SUM = 0
for i in res:
    SUM += i
for i in range(len(res)):
    res[i] /= SUM

print(res)
cv.waitKey(0)