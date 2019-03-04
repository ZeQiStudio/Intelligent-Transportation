'''
Author ambition
Email 957001934@qq.com
Data 2019.2.26
Version 2.0
Fuction 用本地摄像头拍摄视频并保存在本地
'''


import numpy as np
import cv2 as cv

FPS=30
VIDEO_SAVED_URL='C:\\Users\\asus\\Desktop\\camera\\output_video_'
SCREEN_IMG_URL='C:\\Users\\asus\\Desktop\\camera\\image_saved_'

def capture():
    n = 0
    cap = cv.VideoCapture(0)
    size = (int(cap.get(cv.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))
    videoWriter = cv.VideoWriter(VIDEO_SAVED_URL+str(n)+'.avi',
                                 cv.VideoWriter_fourcc('I', '4', '2', '0'), FPS, size)
    sucess, frame = cap.read()
    while sucess:
        videoWriter.write(frame)
        # 转为灰度图片
        #gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        # 显示摄像头，背景是灰度。
        cv.imshow("img", frame)
        # 保持画面的持续。
        k = cv.waitKey(1)
        if k == 27:
            # 通过esc键退出摄像
            cv.destroyAllWindows()
            break
        elif k == ord("s"):
            # 通过s键保存图片
            cv.imwrite(SCREEN_IMG_URL + str(n) + ".jpg", frame)
            n += 1
        sucess, frame = cap.read()
    # 关闭摄像头
    cap.release()

if __name__ == '__main__':
    capture()
