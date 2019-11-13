from django.shortcuts import render

# Create your views here.
# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# 引入我们创建的表单类
from .forms import InfoForm
from All_spider import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def info(request):

    user = request.POST.get("user",'')
    password = request.POST.get("password",'')
    choice = request.POST.get("choice",'')
    print(user,password)
    if user=='' or password=='' or choice=='':
        return HttpResponse(json.dumps({"error":-2}, ensure_ascii=False))
    a = Test()
    info_json = a.main(user,password,choice)
    return HttpResponse(info_json)

