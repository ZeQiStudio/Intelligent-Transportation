'''
author ambition
date 2019.3.24
function 随机选定车辆出现地点
version 1.0
'''

import random
import time
import datetime

address_list=['建设北路二段','建设北路一段','一环路东一段','一环路东二段','猛追湾横街','猛追湾街','游乐园滨河路','华兴路',
         '城隍庙街道','红星路一段','庆云西街','东安南路','书院南路','东风路北一巷']
start = '2019-3-23 07:00:00'
end = '2019-3-23 23:59:59'

def randomDate(start, end,n, frmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(frmt, time.localtime(strTimeProp(start, end, n,frmt)))

def strTimeProp(start, end,n,frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + 0.002 * (etime - stime)*n
    return int(ptime)

def address():
    place=random.sample(address_list,k=1)
    return place[0]

def main():
    clock=randomDate(start,end,1)
    addr=address_list[1]
    return addr,clock


