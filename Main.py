'''
Author ambition
Email 957001934@qq.com
Data 2019.3.2
Function 一些功能调用的实例
'''

from extract_img import Extract
from split_img import Split
from screenshot import Capture
import PlateNumberRecognition.predict as prdc
import cv2 as cv
import yolo.test
import color_recognition
import place_time
import os

IMG_SRC = r'C:\Users\asus\Desktop\test\picture\1 (27).jpg'#图片源
PLATE_NUMBER_PATH=r'C:\Users\asus\Desktop\number_plate\\test\\'#车牌图片保存文件夹
PLATE_NUMBER_IMAGE = r"C:\Users\asus\Desktop\number_plate\number_plate_262.jpg"#车牌号码
SPLITED_PATH=r'C:\Users\asus\Desktop\splited_platenumber\\'#分割好的车牌字符文件夹
VIDEO_SRC=r'C:\Users\asus\Desktop\test\peiqi.avi'#视频源
SCREENSHOT_PATH=r'C:\Users\asus\Desktop\camera\\'#视频截图保存文件夹
FILEDIR=r'C:\Users\asus\Desktop\test\picture'#图片文件夹

if __name__ == '__main__':
    # screen=Capture(VIDEO_SRC,SCREENSHOT_PATH)
    # screen.capture()
    # pics=os.listdir(FILEDIR)
    # for pic in pics:
    #     filename=os.path.join(FILEDIR,pic)#循环读取文件夹
    car_img = cv.imread(IMG_SRC)
    res=yolo.test.check(IMG_SRC)
    number=res.shape[0]
    information = {}
    print('识别出车辆数',number)
    for i in range(number):
        n=str(i)
        information[n]={}
        information[n]['type'] = 'car'
        place,clock=place_time.main()
        information[n]['address']=place
        information[n]['time']=clock
        x=int(res[i][0])
        y=int(res[i][1])
        h=int(res[i][2])#参数的顺序有问题
        w=int(res[i][3])
        # print(x,y,h,w)
        # print('第{}辆车的位置({},{}),宽度{},高度{}'.format(i+1,x,y,w,h))
        # cv.namedWindow('car', flags=0)
        # cv.imshow('car',car_img)
        car=car_img[x-w:x+w,y-h:y+h]
        color_car=color_recognition.color(car)
        information[n]['color']=color_car
        extractd = Extract(car, PLATE_NUMBER_PATH)
        numberimg=extractd.extract()
        # #print(number_plate)
        # split = Split(number_plate, SPLITED_PATH)
        # split.main()
        # cv.namedWindow('car'+str(i)+'.jpg',flags=0)
        # cv.imshow('car'+str(i)+'.jpg',car)
        cv.waitKey(0)
    numberplate = prdc.pdt()
    print(numberplate)
    print(information)

    #车牌提取
    # extractd=Extract(car,PLATE_NUMBER_PATH)
    # extractd.extract()
    # #字符分割
    # split=Split(PLATE_NUMBER_IMAGE,SPLITED_PATH)
    # split.main()
    # print('提取完成')
    #
    # #定时截屏封装版
    # screenshot=Capture(video_path=VIDEO_SRC,screenshot_path=SCREENSHOT_PATH)
    # screenshot.capture()








