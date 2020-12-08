import cv2 as cv
import numpy as np
import os, math

root = 'dataset'
pathList = os.listdir(root)
pathList.append('0')
try:
    for a, files in enumerate(pathList):
        if cv.waitKey(0) & 0xFF == ord('q'):
            cv.waitKey(1)
        elif files:
            # permutations
            src = cv.imread('dataset/' + files, 1)
            dst = np.dot(src[..., :3], [0.299, 0.587, 0.114])
            cv_cvt = cv.cvtColor(src, cv.COLOR_RGB2GRAY)
            cvrt = cv.GaussianBlur(dst, (3, 3), 0)
            canny_cvrt = cv.GaussianBlur(cv_cvt, (3, 3), 0)

            # canny
            w, h = dst.shape
            p = np.zeros([w - 1, h - 1])
            q = np.zeros([w - 1, h - 1])
            m = np.zeros([w, h])
            theta = np.zeros([w, h])
            for i in range(w - 1):
                for j in range(h - 1):
                    p[i, j] = 0.5 * (cvrt[i, j + 1] + cvrt[i + 1, j + 1] - cvrt[i + 1, j] - cvrt[i, j + 1])
                    q[i, j] = 0.5 * (cvrt[i, j] - cvrt[i + 1, j] + cvrt[i, j + 1] - cvrt[i + 1, j + 1])
                    try:
                        m[i, j] = np.sqrt(np.square(p[i, j]) + np.square(q[i, j]))
                        theta[i, j] = math.atan(q[i, j] / p[i, j])
                    except IndexError:
                        m[i, j] = 0
                        theta[i, j] = 0

            w, h = m.shape
            NMS = np.copy(m)
            for i in range(1, w - 1):
                for j in range(1, h - 1):
                    if m[i, j] == 0:
                        NMS[i, j] = 0
                    else:
                        gradPeak = m[i, j]
                        gradDir = math.fabs(math.tan(theta[i, j]))

                        '''ref = [m[round(i+math.cos(theta[i, j])), round(j+math.sin(theta[i, j]))],
                               m[round(i-math.cos(theta[i, j])), round(j-math.sin(theta[i, j]))]]
                        ref = [m[i+1, j], m[i-1, j], m[i+1, j-1], m[i, j-1], m[i+1, j-1],
                               m[i+1, j+1], m[i, j+1], m[i-1, j+1]]

                        for refPoint in ref:
                            if gradPeak < refPoint:
                                NMS[i, j] = 0'''

                        if math.fabs(p[i, j]) > math.fabs(q[i, j]):
                            grad2 = m[i - 1, j]
                            grad4 = m[i + 1, j]
                            if p[i, j] * q[i, j] > 0:
                                grad1 = m[i - 1, j - 1]
                                grad3 = m[i + 1, j + 1]
                            else:
                                grad1 = m[i - 1, j + 1]
                                grad3 = m[i + 1, j - 1]
                        else:
                            grad2 = m[i, j - 1]
                            grad4 = m[i, j + 1]
                            if p[i, j] * q[i, j] > 0:
                                grad1 = m[i + 1, j - 1]
                                grad3 = m[i - 1, j + 1]
                            else:
                                grad1 = m[i - 1, j - 1]
                                grad3 = m[i + 1, j + 1]

                        gradTemp1 = gradDir * grad1 + (1-gradDir) * grad2    # insert value
                        gradTemp2 = gradDir * grad3 + (1-gradDir) * grad4
                        if gradPeak >= gradTemp1 and gradPeak >= gradTemp2:
                            NMS[i, j] = gradPeak
                        else:
                            NMS[i, j] = 0

            w, h = NMS.shape
            dt = np.zeros([w, h])
            tl = 0.1 * np.max(NMS)
            th = 0.3 * np.max(NMS)
            for i in range(1, w - 1):
                for j in range(1, h - 1):
                    if NMS[i, j] < tl:
                        dt[i, j] = 0
                    elif NMS[i, j] > th:
                        dt[i, j] = 1
                    elif ((NMS[i - 1, j - 1:j + 1]).any() or (NMS[i + 1, j - 1:j + 1]).any()
                            or (NMS[i, [j - 1, j + 1]]).any()):
                        dt[i, j] = 1

            '''new_im = Image.fromarray((dt*255).astype(np.uint8))
            plt.imshow(new_im, interpolation='nearest', cmap=plt.cm.gray)
            new_im.show()'''

            # cv.imshow('img', dt)

            # sobel test
            absX = cv.Sobel(dst, cv.CV_16S, 1, 0)
            absY = cv.Sobel(dst, cv.CV_16S, 0, 1)
            sobel = cv.convertScaleAbs(cv.addWeighted(absX, 0.5, absY, 0.5, 0))

            # Filter test
            blur_kernel = np.array((
                [0.0625, 0.125, 0.0625],
                [0.125, 0.25, 0.125],
                [0.0625, 0.125, 0.0625]), dtype="float32")  # blur kernel
            sobel_kernel = np.array((
                [-1, -2, 1],
                [0, 0, 0],
                [1, 2, 1]
            ), dtype="float32")  # sobel kernel
            laplace_kernel = np.array((
                [0, 1, 0],
                [1, -3, 1],
                [0, 1, 0]
            ), dtype="float32")  # laplace kernel(edge checks)
            Filter = cv.filter2D(dt, -1,
                                 kernel=laplace_kernel)  # ddepth(second para)==-1: filtered img&original img have the same depth
            canny = cv.Canny(canny_cvrt, 50, 200)
            print(canny.shape, '\n', dt.shape)
            res = []
            for plc, i in enumerate(canny.flatten()):
                if not i == 0:
                    res.append(i)

            print(len(res))
            res = []
            for plc, i in enumerate(dt.flatten()):
                if not i == 0:
                    res.append(i)

            print(len(res))
            pic = np.hstack([NMS, dt, canny])
            cv.imshow('canny' + files, pic)

except NameError as e:
    print('canny test done *o*')
