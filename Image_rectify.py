'''
Fuction 图象矫正
这个算法还有点问题
'''

import numpy as np
import cv2 as cv
import os

#图片旋转
def rotate_bound(image, angle):
    # 获取宽高
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # 提取旋转矩阵 sin cos
    M = cv.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    # 计算图像的新边界尺寸
    nW=int((h * sin) + (w * cos))
    nH=h
    # 调整旋转矩阵
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv.warpAffine(image, M, (nW, nH), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)

## 获取图片旋转角度
def get_minAreaRect(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.bitwise_not(gray)
    thresh = cv.threshold(gray, 0, 255,
                           cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    return cv.minAreaRect(coords)


image_path = r"C:\Users\asus\Desktop\camera\image_saved_0.jpg"
image = cv.imread(image_path)
angle = get_minAreaRect(image)[-1]
rotated = rotate_bound(image, angle)
cv.imwrite(image_path,rotated)#按原来的名字保存

# show the output image
print("[INFO] angle: {:.3f}".format(angle))
cv.imshow("imput", image)
cv.imshow("output", rotated)
cv.waitKey(0)
