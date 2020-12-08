import numpy as np
import math
import cv2 as cv
import os


def GaussianBlurMatrix(sigma=1.0,
                       default=5):  # sigma = pow(pow(2, interval/(G-3)), interval), G = the number of intervals in each octave
    total = 0
    gaussian = np.zeros([default, default])  # for gaussian matrix at 5*5, the center point is (3, 3)
    for ix in range(default):
        for j in range(default):
            gaussian[ix, j] = math.exp(-1 / 2 * (np.square(ix - 3) + np.square(j - 3)) / np.square(sigma)) / (
                    2 * math.pi * np.square(sigma))
            total += gaussian[ix, j]

    gaussian = gaussian / total  # normalize the coefficients
    return gaussian


GS8 = GaussianBlurMatrix(0.5, 16)


def GaussianBlur(grayImg, times=1, sigma=1):
    while times:
        grayImg = cv.GaussianBlur(grayImg, (5, 5), sigma)
        times -= 1
    return grayImg


def degradedSampling(grayImg):
    deg = cv.pyrDown(grayImg)
    return deg


def DOG(img1, img2):
    w1, h1 = img1.shape
    w2, h2 = img2.shape
    if not (w1 == w2 and h1 == h2):
        print("DOG error")
        return img1
    else:
        w, h = w1, h1
        newPic = np.zeros([w, h])
        for x in range(w):
            for y in range(h):
                newPic[x, y] = img2[x, y] - img1[x, y]

    return newPic


def keyPointCompare(imgOri, imgComp1, imgComp2):
    w, h = imgOri.shape
    r0 = 10
    KP = list()
    for x in range(w - 1):
        for y in range(h - 1):
            comp = [imgOri[x - 1, y - 1], imgOri[x, y - 1], imgOri[x + 1, y - 1], imgOri[x - 1, y], imgOri[x + 1, y],
                    imgOri[x - 1, y + 1],
                    imgOri[x, y + 1], imgOri[x + 1, y + 1], imgComp1[x - 1, y - 1], imgComp1[x, y - 1],
                    imgComp1[x + 1, y - 1],
                    imgComp1[x - 1, y], imgComp1[x + 1, y], imgComp1[x - 1, y + 1], imgComp1[x, y + 1],
                    imgComp1[x + 1, y + 1], imgComp1[x, y],
                    imgComp2[x - 1, y - 1], imgComp2[x, y - 1], imgComp2[x + 1, y - 1], imgComp2[x - 1, y],
                    imgComp2[x + 1, y], imgComp2[x - 1, y + 1],
                    imgComp2[x, y + 1], imgComp2[x + 1, y + 1], imgComp2[x, y]]
            if imgOri[x, y] > np.max(comp):
                dx = imgOri[x + 1, y] - imgOri[x, y]
                dy = imgOri[x, y + 1] - imgOri[x, y]
                s = np.sqrt(np.square(dx) + np.square(dy))
                D = s + s * imgOri[x, y]
                d2x = imgOri[x + 1, y] + imgOri[x - 1, y] - 2 * imgOri[x, y]
                d2y = imgOri[x, y + 1] + imgOri[x, y - 1] - 2 * imgOri[x, y]
                dxy = imgOri[x + 1, y + 1] + imgOri[x, y] - imgOri[x, y + 1] - imgOri[x + 1, y]
                Tr = d2x + d2y;
                Det = d2x * d2y - np.square(dxy)
                if Det == 0:
                    continue
                elif np.square(Tr) / Det < np.square(r0 + 1) / r0 and D >= 0.3 * np.max(D):
                    KP.append((x, y))
                    # print(f'found[{x}, {y}]')

    return KP


def SIFTdescriptor(imgCoord, imgS,
                   box=8):  # imgCoord only feeds in the coordinates, the the coordinates is compared with imgS
    try:
        x0 = imgCoord[0] - 4
        y0 = imgCoord[1] - 4  # amending the loss of x y coordinates
        bins = [0] * box  # box = 8, bins is the 8 dir vector

        m = np.zeros([8, 8])
        theta = np.zeros([8, 8])
        for x in range(8):
            for y in range(8):
                dx = imgS[x0 + x + 1, y0 + y] - imgS[x0 + x - 1, y0 + y]
                dy = imgS[x0 + x, y0 + y + 1] - imgS[x0 + x, y0 + y - 1]
                m[x, y] = np.sqrt(np.square(dx) + np.square(dy))
                flag = (dx * dy > 0)
                if imgS[x0 + x + 1, y0 + y] - imgS[x0 + x - 1, y0 + y] == 0:
                    theta[x, y] = (math.pi / 2) * (2 * flag - 1)
                else:
                    theta[x, y] = math.atan((imgS[x0 + x, y0 + y + 1] - imgS[x0 + x, y0 + y - 1]) / (
                            imgS[x0 + x + 1, y0 + y] - imgS[x0 + x - 1, y0 + y])) * (2 * flag - 1)

                for idx in range(box):
                    if -180 + (360 / box) * idx < theta[x, y] * 180 / math.pi <= -180 + (360 / box) * (idx + 1):
                        bins[idx] += m[x, y]

        max_bin_value = 0
        idx = 0
        for i0 in range(box):
            if np.abs(bins[i0]) > max_bin_value:
                max_bin_value = bins[i0]
                idx = i0

    except IndexError:
        return 0, 0

    return max_bin_value, idx


def ImageDescriptor(lis, cprt, Img):
    try:
        f = 0
        averX = averY = 0
        for i in lis:
            x0 = int(i[0] - 8)
            y0 = int(i[1] - 8)  # amending the loss of x y coordinates

            for x in range(16):
                for y in range(16):
                    dx = Img[x0 + x + 1, y0 + y] - Img[x0 + x - 1, y0 + y]
                    dy = Img[x0 + x, y0 + y + 1] - Img[x0 + x, y0 + y - 1]
                    averX += np.sqrt(np.square(dx) + np.square(dy))

        for i in cprt:
            x0 = int(i[0] - 8)
            y0 = int(i[1] - 8)  # amending the loss of x y coordinates

            for x in range(16):
                for y in range(16):
                    dx = Img[x0 + x + 1, y0 + y] - Img[x0 + x - 1, y0 + y]
                    dy = Img[x0 + x, y0 + y + 1] - Img[x0 + x, y0 + y - 1]
                    averY += np.sqrt(np.square(dx) + np.square(dy))
        for f0 in range(1000):
            if 0.1 * f0 < averX / averY <= 0.1 + 0.1 * f0:
                f = f0
    except IndexError:
        return 0
    return f


def mainFunction(gray):
    interval1 = list()
    default_interval = 6
    i = 0

    while i < default_interval:  # octave 1
        gbPic = GaussianBlur(gray, i, round(pow(2, i / 3)))
        interval1.append(gbPic)
        '''if i == 3:
            octave.append(degradedSampling(gbPic))'''  # test sample only take octave=1
        i += 1

    for i in range(default_interval - 1):  # differentiate of Gaussian matrix
        interval1[i] = DOG(interval1[i], interval1[i + 1])

    KPlist = list()
    for i in range(2, default_interval - 2):
        KPmat = keyPointCompare(interval1[i], interval1[i - 1], interval1[i + 1])
        KPlist.append(KPmat)

    keyPointStack = list()
    keyPointAngle = list()
    amps = list()
    gray = np.float32(gray)
    corners = np.int0(cv.goodFeaturesToTrack(gray, 20, 0.01, 10))

    for index in corners:
        i = index.flatten()
        # box = (36 if isOrigin else 8)
        maxValue, angle = SIFTdescriptor(i, gray)
        keyPointAngle.append(angle * math.pi / 4)
        keyPointStack.append(i)
        amps.append(maxValue)

    return keyPointStack, keyPointAngle, amps


img = cv.imread('target.jpg')  # main function
root = 'dataset'
pathList = os.listdir(root)
gray1 = np.dot(img[..., :3], [0.299, 0.587, 0.114])
W1, H1 = gray1.shape
kps1, aver1, amp1 = mainFunction(gray1)


def function(image1, image2):
    h1, w1, c1 = image1.shape
    h2, w2, c2 = image2.shape
    if c1 != c2:
        return
    else:
        if w1 > w2:
            tmp = np.zeros([h2, w1 - w2, c1])
            image3 = np.hstack([image2, tmp])
            image3 = np.vstack([image1, image3])
        elif w1 == w2:
            image3 = np.vstack([image1, image2])
        else:
            tmp = np.zeros([h1, w2 - w1, c2])
            image3 = np.hstack([image1, tmp])
            image3 = np.vstack([image3, image2])
    return image3


for path, files in enumerate(pathList):
    cpr = cv.imread('dataset/' + files)
    gray2 = np.dot(cpr[..., :3], [0.299, 0.587, 0.114])

    kps2, aver2, amp2 = mainFunction(gray2)
    cvrt = list()
    ss = 0
    W2, H2 = gray2.shape
    for Id in kps1:
        s = [0, 0]
        angleDiff = aver1[ss] - aver2[ss]
        s[0] = round((Id[0] * math.cos(angleDiff) - Id[1] * math.sin(angleDiff)) * W2 / W1)
        s[1] = round((Id[0] * math.sin(angleDiff) + Id[1] * math.cos(angleDiff)) * H2 / H1)
        while s[0] < 0 or s[1] < 0:
            s[0] = (s[0] + W2 if s[0] < 0 else s[0])
            s[1] = (s[1] + H2 if s[1] < 0 else s[1])
        cvrt.append(s)
        ss += 1

    '''print("kps1 ", kps1)
    print("aver1 ", aver1)
    print("dst ", dst)
    print("cvrt ", cvrt)
    print("kps2 ", kps2)
    print("aver2 ", aver2)'''

    ff = ImageDescriptor(cvrt, kps2, gray2)
    print('dataset/' + files, ': ', ff)

    cpr = cv.resize(cpr, (512, 512))
    img = cv.resize(img, (512, 512))
    x = np.vstack([img, cpr])
    for i in range(len(kps1) if len(kps1) < len(kps2) else len(kps2)):
        x1, y1 = kps1[i]
        x2, y2 = kps2[i]
        cv.circle(x, (x1, y1), 3, (0, 0, 255), -1)
        cv.circle(x, (x2, y2 + 512), 3, (255, 0, 0), -1)
        cv.line(x, (x1, y1), (x2, y2 + H1), (0, 255, 0))

    cv.imshow('x', x)
    cv.waitKey(0)
