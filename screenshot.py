'''
Author ambition
Email 957001934@qq.com
Data 2019.3.2
Version 2.0(封装版)
Fuction 定时截图 从本地读取视频文件，按一定时间间隔截取图片
'''

import numpy as np
import cv2 as cv
import time
import threading
import sys

class Capture:
    def __init__(self,video_path,screenshot_path):
        self.n = 0
        self.SCREENSHOT_PATH=screenshot_path
        self.cap = cv.VideoCapture(video_path)

        # fps=cap.get(cv.CAP_PROP_FPS)#获取视频的帧数
        # print(fps) #视频fps是30

    def capture(self):
        num = 0
        sucess, frame = self.cap.read()
        # 计算运行时间
        # t0 = time.clock()

        while sucess:
            # cv.imshow("img", frame)
            # 保持画面的持续。
            k = cv.waitKey(1)
            self.n += 1

            if k == 27:
                # 通过esc键退出摄像
                cv.destroyAllWindows()
                sys.exit()

            if self.n % (180) == 0:
                # print(n)
                cv.imwrite(self.SCREENSHOT_PATH +'image_saved_'+str(num) + ".jpg", frame)
                num += 1
                # t1 = time.clock()
                # print(t1 - t0)

            sucess, frame = self.cap.read()
        print("视频图象截取完毕")
        self.cap.release()
        cv.destroyAllWindows()
        sys.exit()



