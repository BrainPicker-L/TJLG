# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse

# 引入我们创建的表单类
from .forms import AddForm
from All_spider import *
def library(request):
    if request.method == 'GET':# 当提交表单时

        form = AddForm(request.GET) # form 包含提交的数据

        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            library = Library()
            books_info_json = library.getBookinfo(a,b)
            return HttpResponse(books_info_json)

    else:# 当正常访问时
        form = AddForm()
    return render(request, 'lib_search.html', {'form': form})
