'''
author ambition
date 2019.3.24
function 车辆颜色识别
version 2.0封装版
'''

import numpy as np
import cv2 as cv

#颜色HSV范围
red_min = np.array([0, 128, 46])
red_max = np.array([5, 255,255])
#橙色
orange_min = np.array([156,128,46])
orange_max = np.array([180,255,255])

green_min = np.array([35, 128, 46])
green_max = np.array([77, 255, 255])

blue_min=np.array([100,128,46])
blue_max=np.array([124,255,255])


yellow_min = np.array([15, 128, 46])
yellow_max = np.array([34, 255, 255])

black_min=np.array([0,0,0])
black_max = np.array([180,255,10])

white_min=np.array([0,0,70])
white_max=np.array([180,30,255])

COLOR_ARRAY=[[red_min,red_max,'red'],[orange_min,orange_max,'orange'],[green_min,green_max,'green'],[blue_min,blue_max,'blue'],[yellow_min,yellow_max,'yellow'],[black_min,black_max,'black'],[white_min,white_max,'white']]

def color(frame):
    # frame = cv.imread(scr_img)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # cv.imshow("hsv.jpg",hsv)

    for (color_min, color_max, name) in COLOR_ARRAY:
        mask = cv.inRange(hsv, color_min, color_max)
        res = cv.bitwise_and(frame, frame, mask=mask)

        #前面是为了得到一张二值图
        img = res
        h,w= img.shape[:2]

        blured = cv.GaussianBlur(img, (3, 3), 0)  # 过滤
        ret, bright = cv.threshold(blured, 0, 255, cv.THRESH_BINARY)  # 二值化
        gray = cv.cvtColor(bright, cv.COLOR_BGR2GRAY)  # 转灰度
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (50, 50))
        opened = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)  # 开操作
        # cv.imshow("opened.jpg", opened)
        closed = cv.morphologyEx(opened, cv.MORPH_CLOSE, kernel)  # 闭操作
        # cv.imshow("closed.jpg", closed)

        contours, hierarchy = cv.findContours(closed, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        # cv.drawContours(img,contours,-1,(0,0,255),3)
        # cv.imshow("result.jpg",img)
        # 输出轮廓个数
        number = len(contours)
        # print('Total:', number)
        if number >= 1:
            total = 0
            for i in range(0, number):
                # len(contours[i]为轮廓区域的像素点深度个数
                total = total + len(contours[i])
                # print('NO:',i,' size:',len(contours[i]))
                if total > 400:  # 如果所有该颜色区域的像素加起来超过400，则认为是该颜色
                    # print('Currrent color is ', name)
                    cv.waitKey(0)
                    cv.destroyAllWindows()
                    return name
