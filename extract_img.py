'''
Author ambition
Email 957001934@qq.com
Data 2019.2.26
Version 4.0（封装版）
Function 进行图片预处理并提取图片中的车牌号码区域图片
Notes 由于数据不固定所以还需要调整参数
'''

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os

class Extract:
    IMAGE_SRC =''
    NUMBER_PLATE_SAVE_URL =''
    NEW_WIDTH = 233
    NEW_HEIGHT = 73
    def __init__(self,img_src,img_saved):
        # self.IMAGE_SRC=img_src
        self.NUMBER_PLATE_SAVE_URL=img_saved
        isExisted2=os.path.exists(img_saved)
        # if not isExisted1:
        #     print('图片源不存在，请确认图片路径输入正确')
        if not isExisted2:
            print('图片保存路径不存在，请确认图片保存路径正确')
        self.img=img_src



    def img_info(self,img):
        print(type(img))
        print(img.shape)
        print(img.size)  # 长*宽*通道数
        print(img.dtype)  # 编码格式
        pixel_data=np.array(img)#转换为array的像素信息
        print(pixel_data)


    # 图象大小改变
    def resized(self,img):
        temp = img.copy()
        h = temp.shape[0]
        w = temp.shape[1]
        print(w, h)
        m = 400 * h / w
        # 压缩图像
        new_img = cv.resize(temp, (400, int(m)), interpolation=cv.INTER_CUBIC)
        #cv.imshow('new_img', new_img)
        return new_img

    # 直方图均衡化
    def equalHist(self,img):
        # gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        dst = cv.equalizeHist(img)
        # cv.imshow('equalHist',dst)
        return dst

    # 图片的一系列形态学操作
    # input 读取后的图片
    # output 轮廓信息
    def preprocess(self,img):
        # img_info(img)查看图片信息
        # 高斯模糊去噪
        gaussian = cv.GaussianBlur(img, (3, 3), 0)
        hsv = cv.cvtColor(gaussian, cv.COLOR_BGR2HSV)
        blue_lower_hsv = np.array([100, 43, 46])
        blue_upper_hsv = np.array([124, 255, 255])
        yellow_lower_hsv = np.array([26, 43, 46])
        yellow_upper_hsv = np.array([34, 255, 255])
        mask = cv.inRange(hsv, blue_lower_hsv, blue_upper_hsv)
        if mask.all():
            mask = cv.inRange((hsv, yellow_lower_hsv, yellow_upper_hsv))
        # cv.imshow('mask', mask)
        # 直方图均衡化
        # equalhist=equalHist(mask)
        # cv.imshow('equalhist',equalhist)

        # 闭操作
        kernelX = cv.getStructuringElement(cv.MORPH_RECT, (17, 5))
        close = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernelX)

        # cv.imshow('close',close)
        open = cv.morphologyEx(close, cv.MORPH_OPEN, kernel=kernelX)

        # 膨胀和腐蚀
        kernel_X = cv.getStructuringElement(cv.MORPH_RECT, (20, 1))
        kernel_Y = cv.getStructuringElement(cv.MORPH_RECT, (1, 19))
        dilate1 = cv.dilate(open, kernel_X)
        erode1 = cv.erode(dilate1, kernel_X)

        # 平滑处理，中值滤波
        blurred = cv.medianBlur(erode1, 15)
        # cv.imshow('blurred',blurred)

        # 查找轮廓
        contours, hierarchy = cv.findContours(blurred, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours

    # 通过轮廓判断找出车牌
    # input 可疑轮廓列表
    # output 车牌
    def contour_judge(self,contours):
        # print(type(contours))查看轮廓信息
        # print(contours)
        for item in contours:
            rect = cv.boundingRect(item)
            x = rect[0]
            y = rect[1]
            weight = rect[2]
            height = rect[3]
            if weight > (height * 2) and weight < (height * 5):  # 中国车牌一般宽:高为2.7-5
                # 裁剪区域图片
                number_plate = self.img[y:y + height, x:x + weight]
                #print(number_plate.shape[:2])
                if number_plate.shape[1] > (number_plate.shape[0] * 3) and (number_plate.shape[0] * 4.5) > (
                number_plate.shape[1]):
                    # number_plate = self.resized(number_plate)
                    number_plate_path=self.NUMBER_PLATE_SAVE_URL + 'number_plate_' + str(x) + '.jpg'
                    cv.imwrite(number_plate_path, number_plate)
                    # cv.imshow('number_plate' + str(x) + '.jpg', number_plate)#展示提取出的车牌截图
                    cv.waitKey(0)
                    return number_plate

    def extract(self):
        #cv.imshow('scr_img', self.img)
        # img = resized(img)
        contours = self.preprocess(self.img)
        number_plate=self.contour_judge(contours)
        # print('车牌提取完毕')
        # 可视化操作
        cv.waitKey(0)
        cv.destroyAllWindows()
        return number_plate