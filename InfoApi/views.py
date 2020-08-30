from django.shortcuts import render

# Create your views here.
# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import spider_test

# 引入我们创建的表单类
from .forms import InfoForm
from All_spider import *
from django.views.decorators.csrf import csrf_exempt
from InfoApi.models import *
@csrf_exempt
def info(request):

    user = request.POST.get("user",'')
    password = request.POST.get("password",'')
    choice = request.POST.get("choice",'')
    print(user,password)
    if user=='' or password=='' or choice=='':
        return HttpResponse(json.dumps({"error":-2}, ensure_ascii=False))
    info_json = spider_test.main(user,password,choice)
    return HttpResponse(info_json)

def get_start_school_day(request):
    start_school_day_obj = StartSchoolDay.objects.all()
    if len(start_school_day_obj) == 0:
        return HttpResponse(json.dumps({"error": "没有设置开学日期"}, ensure_ascii=False))
    else:
        start_school_day_obj = start_school_day_obj[0]
        return HttpResponse(json.dumps({"start_school_day":"%s-%s-%s"%(start_school_day_obj.time.year,start_school_day_obj.time.month,start_school_day_obj.time.day)}, ensure_ascii=False))