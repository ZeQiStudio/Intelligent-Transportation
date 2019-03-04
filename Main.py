'''
Author ambition
Email 957001934@qq.com
Data 2019.3.2
Function 一些功能调用的实例
'''

from extract_img import Extract
from split_img import Split
from screenshot import Capture

IMG_SRC = r'C:\Users\asus\Desktop\test\1.jpg'#图片源
PLATE_NUMBER_PATH=r'C:\Users\asus\Desktop\number_plate\\'#车牌图片保存文件夹
PLATE_NUMBER_IMAGE = r"C:\Users\asus\Desktop\number_plate\number_plate_1696.jpg"#车牌号码
SPLITED_PATH=r'C:\Users\asus\Desktop\splited_platenumber\\'#分割好的车牌字符文件夹
VIDEO_SRC=r'C:\Users\asus\Desktop\test\peiqi.avi'#视频源
SCREENSHOT_PATH=r'C:\Users\asus\Desktop\camera\\'#视频截图保存文件夹


if __name__ == '__main__':

    #车牌提取
    extractd=Extract(IMG_SRC,PLATE_NUMBER_PATH)
    extractd.extract()
    #字符分割
    split=Split(PLATE_NUMBER_IMAGE,SPLITED_PATH)
    split.main()
    print('提取完成')

    #定时截屏封装版
    screenshot=Capture(video_path=VIDEO_SRC,screenshot_path=SCREENSHOT_PATH)
    screenshot.capture()





