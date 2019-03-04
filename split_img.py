'''
Author ambition
Email 957001934@qq.com
Data 2019.2.26
Version 3.0（封装版）
Function 分割车牌号码，输出分割好的每一个字符图片
'''

import cv2 as cv
import numpy as np
import os

class Split:
    WIDTH = 32
    HEIGHT = 40
    IMAGE_PATH =''
    SAVE_SPLITED_URL =''
    order=0

    def __init__(self,image_path,splited_saved):
        self.IMAGE_PATH=image_path
        self.SAVE_SPLITED_URL=splited_saved
        self.img = cv.imread(image_path)
        # 生成保存文件
        self.file_path = self.mkdir_file()


    # 亮度对比度调整
    def contrast_lightness(self,img, c, b):  # c为对比度增强倍数，b为亮度增强倍数
        h, w, channel = img.shape
        blank = np.zeros([h, w, channel], img.dtype)
        dst = cv.addWeighted(img, c, blank, 1 - c, b)
        # cv.imshow('dst',dst)
        return dst

    def resized(self,img):
        # cv.imshow('old_img',img)
        resized_img = cv.resize(img, (self.WIDTH, self.HEIGHT))
        return resized_img

    def preprocess(self,img):
        # 转灰度
        image = self.contrast_lightness(img, 1.5, 2)
        # cv.imshow('new_img',image)

        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # cv.imshow('gray',gray)

        # 二值化
        ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        # 腐蚀膨胀
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))  # 卷积核

        dilate1 = cv.dilate(binary, kernel=kernel)
        # cv.imshow('dilate1',dilate1)
        erode1 = cv.erode(dilate1, kernel=kernel)
        # cv.imshow('erode1', erode1)
        dilate2 = cv.dilate(erode1, kernel=kernel)
        # cv.imshow('dilate2',dilate2)

        return dilate2, binary

    def save_splited_img(self,splited_img, order):
        # cv.imshow('splited_img',splited_img)
        new_img = self.resized(splited_img)
        # cv.imshow('new_splited_img',new_img)
        cv.imwrite(self.file_path + str('\\') + str(order) + '.jpg', new_img)


    def mkdir_file(self):
        number_plate_flie = self.IMAGE_PATH.split('\\')[-1].split('.')[0]
        file_path = self.SAVE_SPLITED_URL + str(number_plate_flie)
        isExisted = os.path.exists(file_path)
        if not isExisted:
            os.makedirs(file_path)
            print('创建车牌字符分割文件夹成功')
        else:
            print('该车牌字符分割文件夹已存在')
        return file_path

    def split(self,preprocessed,binary):
        white = []  # 记录每一列的白色像素总和
        black = []  # ..........黑色.......
        height = preprocessed.shape[0]
        width = preprocessed.shape[1]
        white_max = 0
        black_max = 0
        # 计算每一列的黑白色像素总和
        for i in range(width):
            s = 0  # 这一列白色总数
            t = 0  # 这一列黑色总数
            for j in range(height):
                if preprocessed[j][i] == 255:
                    s += 1
                if preprocessed[j][i] == 0:
                    t += 1
            white_max = max(white_max, s)
            black_max = max(black_max, t)
            white.append(s)
            black.append(t)
            # print(s)
            # print(t)

        arg = False  # False表示白底黑字,True表示黑底白字
        if black_max > white_max:
            arg = True

        # 分割图像
        def find_end(start):
            end = start + 1
            for m in range(start + 1, width - 1):
                if (black[m] if arg else white[m]) > (
                        0.9 * black_max if arg else 0.9 * white_max):  # 0.95这个参数请多调整，对应下面的0.05
                    end = m
                    break
            return end
        order = 0
        n = 1
        start = 1
        end = 2
        while n < width - 2:
            n += 1
            if (white[n] if arg else black[n]) > (0.1 * white_max if arg else 0.1 * black_max):
                start = n
                end = find_end(start)
                n = end

                if end - start > 5:
                    splited_img = binary[1:height, start:end]
                    #cv.imshow('splited_img', splited_img)#分割出的字符图片
                    self.save_splited_img(splited_img, order)
                    order += 1

    def main(self):
        # cv.imshow('scr_img',self.image)
        # 车牌提取
        preprocessed, binary = self.preprocess(self.img)
        # 字符分割
        self.split(preprocessed,binary)
        print('字符分割完毕')
        # 图象持久化操作
        cv.waitKey(0)
        cv.destroyAllWindows()