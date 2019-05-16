import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NewProject.settings")
django.setup()
import datetime
import json

import simplejson as simplejson


from django.http import HttpResponse
from django.shortcuts import render

from TestModel.models import Test2,  Test3
from TestModel.models import Test4

json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)
def Login(request):
    if request.method=='POST':
        req = simplejson.loads(request.raw_post_data)
        username = req['username']
        password = req['password']
        user = Test2.objects.filter(username=username, password=password)
        if user:
            result=1
            return HttpResponse(json.dumps({
                "result":result
            }))
        result=0
        return HttpResponse(json.dumps({
            "result":result
        }))

def chuanghongdeng(request):
    if request.method == 'GET':
        json_list = []
        obj1s = Test3.objects.filter(site='二环路东二段').order_by("time")
        m=0
        id=1
        for obj1 in obj1s:
            obj2s = Test4.objects.filter(carid=obj1.carid)
            json_dict = {}
            for obj2 in obj2s:
                json_dict["id"]=id
                json_dict["location"] = obj1.site
                json_dict["time"] = obj1.time
                json_dict["name"] = obj2.name
                json_dict["carID"] = obj1.carid
                print(obj1.site)
                m = m + 1
                json_list.append(json_dict)
        xixixi = {}
        xixixi["number"] = m
        json_list.append(xixixi)
        return HttpResponse(json.dumps(json_list), content_type="application/json")
'''
def chuanghongdeng(self,request):
    if request.method=='GET':
        req = simplejson.loads(request.raw_post_data)
        type=req['type']
        json_list=[]
        if type==1:
            m=0
            location=req['location']
            obj1s = Test3.objects.filter(site=location).order_by("time")
            for obj1 in obj1s:
                obj2s = Test4.objects.filter(carID=obj1.carID)
                json_dict={}
                for obj2 in obj2s:
                    json_dict["location"] = obj1.site
                    json_dict["time"]=obj1.time
                    json_dict["name"]=obj2s.name
                    json_dict["carID"]=obj1.carID
                    m=m+1
                    json_list.append(json_dict)
            xixixi = {}
            xixixi["number"] = m
            json_list.append(xixixi)
            return HttpResponse(json.dumps(json_list), content_type="application/json")
        elif type==2:
            times=req['times']
            timee=req['timee']
            s=[]
            d=[]
            s = times.split('-')
            d = timee.split('-')
            yf=s[0]
            mf=s[1]
            df=s[2]
            minf=s[3]
            sef=s[4]
            yt = d[0]
            mt = d[1]
            dt = d[2]
            mint = d[3]
            set = d[4]
            date_from = datetime.datetime(int(yf), int(mf), int(df), int(minf), int(sef))
            date_to = datetime.datetime(int(yf), int(mf), int(df), int(minf), int(sef))
            obj1s = Test3.objects.filter(CarTime__range=(date_from, date_to)).order_by("time")
            m=0
            for obj1 in obj1s:
                json_dict = {}
                obj2s = Test4.objects.filter(carID=obj1.carID)
                for obj2 in obj2s:
                    json_dict["location"] = obj1.site
                    json_dict["time"] = obj1.time
                    json_dict["name"] = obj2s.name
                    json_dict["carID"] = obj1.carID
                    m=m+1
                    json_list.append(json_dict)
            xixixi = {}
            xixixi["number"] = m
            json_list.append(xixixi)
            return HttpResponse(json.dumps(json_list), content_type="application/json")
        elif type==3:
            name=req["name"]
            json_list = []
            obj1s = Test4.objects.filter(name=name)
            m=0
            for obj1 in obj1s:
                json_dict={}
                obj2s=Test3.objects.filter(carID=obj1.carID)
                for obj2 in obj2s:
                    json_dict["name"]=obj1.name
                    json_dict["location"]=obj2.site
                    json_dict["time"]=obj2.time
                    json_dict["carID"]=obj2.carID
                    m=m+1
                    json_list.append(json_dict)
            xixixi={}
            xixixi["number"]=m
            json_list.append(xixixi)
            return HttpResponse(json.dumps(json_list), content_type="application/json")
'''
def CarRoute(request):
    if request.method=='GET':
        req = simplejson.loads(request.raw_post_data)
        carID=req['carID']
        times = req['times']
        timee = req['timee']
        s = []
        d = []
        s = times.split('-')
        d = timee.split('-')
        yf = s[0]
        mf = s[1]
        df = s[2]
        minf = s[3]
        sef = s[4]
        yt = d[0]
        mt = d[1]
        dt = d[2]
        mint = d[3]
        set = d[4]
        date_from = datetime.datetime(int(yf), int(mf), int(df), int(minf), int(sef))
        date_to = datetime.datetime(int(yf), int(mf), int(df), int(minf), int(sef))
        obj1s = Test3.objects.filter(CarTime__range=(date_from, date_to),carID=carID).order_by("time")
        str1="["
        ajing=0
        awei=0
        n=0
        a1="\""
        bb=[]
        for obj1 in obj1s:
            jingdu=obj1.jingdu
            weidu=obj1.weidu
            ajing=ajing+jingdu
            awei=awei+weidu
            a2=str(jingdu)
            a3=str(weidu)
            n=n+1
            str1+=a2
            str1+="|"
            str1+=a3
            bb.append(str1)
            #str1+=a3
        #str1 += "]"
        jd = ajing / n
        wd = awei / n
        str5=""
        str3=str(jd)
        str4=str(wd)
        str5+=str3
        str5+="|"
        str5+=str4
        return render(request, 'hhh.html', context={
            'hehe': str5,
            'bb': bb
        })






