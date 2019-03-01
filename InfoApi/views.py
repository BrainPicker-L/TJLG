from django.shortcuts import render

# Create your views here.
# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# 引入我们创建的表单类
from .forms import InfoForm
from All_spider import *
def info(request):
    if request.method == 'POST':# 当提交表单时
        form = InfoForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            choice = form.cleaned_data['choice']
            a = Test()
            info_json = a.main(user,password,choice)
            return HttpResponse(info_json)

    else:# 当正常访问时
        form = InfoForm()
    return render(request, 'test_search.html', {'form': form})
