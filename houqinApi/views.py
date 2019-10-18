from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import *
import time
from .forms import *
from django.http import HttpResponse
import random
import json
from django.core.paginator import Paginator
from fuzzywuzzy import fuzz

def houqin_home(request):
    context = {}
    if request.user.username == "后勤管理处综合信息中心":
        context["search_form"] = SearchForm()



        if request.method == "GET":
            status = request.GET.get('status','未处理')
            context["status_now"] = status
            searchtext = request.GET.get('searchtext','')
            context["searchtext"] = searchtext
            if searchtext!="":
                context["gongdans"] = Gongdan.objects.filter(gongdanid__contains=searchtext).order_by('-created_time')
                return render(request, 'houqin_home.html', context)
            else:
                if status == "未处理":
                    context["gongdans"] = Gongdan.objects.filter(status__name="未处理").order_by('-created_time')

                elif status == "已处理":
                    context["gongdans"] = Gongdan.objects.filter(status__name="已处理").order_by('-created_time')

                elif status == "已收录":
                    context["gongdans"] = Gongdan.objects.filter(status__name="已收录").order_by('-created_time')

        #分页
        paginator = Paginator(context["gongdans"], 5)
        page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
        page_of_gongdans = paginator.get_page(page_num)
        currentr_page_num = page_of_gongdans.number  # 获取当前页码
        # 获取当前页码前后各2页的页码范围
        page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                     list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
        # 加上省略页码标记
        if page_range[0] - 1 >= 2:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append('...')
        # 加上首页和尾页
        if page_range[0] != 1:
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)
        context['gongdans'] = page_of_gongdans.object_list
        context['page_of_gongdans'] = page_of_gongdans
        context['page_range'] = page_range
    return render(request, 'houqin_home.html', context)



def houqin_detail(request,gd_pk):   #传入参数工单pk
    context={}

    context["select_form"] = SelectForm()
    if request.method == "POST":
        status_pk = request.POST.get("sel_value2", StatusName.objects.get(name="未处理").pk)
        gd_pk = request.POST.get("gd_pk", '')
        status = request.POST.get("status", '未处理')
        reply = request.POST.get("reply", '')
        context["status_now"] = status
        obj = Gongdan.objects.get(pk=gd_pk)
        obj.status = StatusName.objects.get(pk=status_pk)
        obj.reply = reply
        obj.save()
        context["gongdan"] = Gongdan.objects.get(id=int(gd_pk))

    elif request.method == "GET":
        context["gongdan"] = Gongdan.objects.get(id=int(gd_pk))
    print(gd_pk)
    return render(request, 'houqin_detail.html', context)



@csrf_exempt
def add_gongdan(request):
    sno = request.POST.get('sno','')
    name = request.POST.get('name','')
    excerpt = request.POST.get('excerpt','')
    phone_num = request.POST.get('phone_num','')
    if not (sno and name and excerpt):
        return HttpResponse(json.dumps({"error":"所有字段不能为空"}, ensure_ascii=False))
    obj = Gongdan()
    obj.gongdanid = time.strftime("%Y%m%d")+sno+str(len(Gongdan.objects.all())).zfill(6)
    obj.sno = sno
    obj.name = name
    obj.phone_num = phone_num
    obj.excerpt = excerpt
    obj.status = StatusName.objects.get(name="未处理")
    obj.save()
    return HttpResponse(json.dumps({"success": "已记录，可在维修进度中查看"}, ensure_ascii=False))


def person_gongdan_status(request):
    sno = request.GET.get('sno','')
    if sno == '':
        return HttpResponse(json.dumps({"error":"所有字段不能为空"}, ensure_ascii=False))
    gongdan_lst = Gongdan.objects.filter(sno=sno).order_by('-created_time')
    all_lst = []
    for gongdan in gongdan_lst:

        all_lst.append({
            'gongdanid':gongdan.gongdanid,
            'excerpt':gongdan.excerpt,
            'reply':gongdan.reply,
        'status':gongdan.status.name,
        'created_time':str(gongdan.created_time).split('.')[0],
        })
    return HttpResponse(json.dumps(all_lst, ensure_ascii=False))



def gongdan_detail(request):
    gongdanid = request.GET.get('gongdanid','')
    if gongdanid == '':
        return HttpResponse(json.dumps({"error":"所有字段不能为空"}, ensure_ascii=False))
    gongdan = Gongdan.objects.get(gongdanid=gongdanid)

    return HttpResponse(json.dumps({
            'gongdanid': gongdan.gongdanid,
            'name':gongdan.name[0]+"同学",
            'excerpt': gongdan.excerpt,
            'reply': gongdan.reply,
            'status': gongdan.status.name,
            'created_time': str(gongdan.created_time).split('.')[0],
        }, ensure_ascii=False))


def all_gongdan(request):
    searchtext = request.GET.get("searchtext", '')
    if searchtext!='':
        gongdan_all_list = Gongdan.objects.filter(status=StatusName.objects.get(name="已收录")).order_by("-created_time")
        list1 = []
        for gongdan in gongdan_all_list:
            if searchtext in gongdan.excerpt:
                dict1 = {
                'gongdanid': gongdan.gongdanid,
                'name':gongdan.name[0]+"同学",
                'excerpt': gongdan.excerpt,
                'reply': gongdan.reply,
                'status': gongdan.status.name,
                'created_time': str(gongdan.created_time).split('.')[0],
                }
                list1.append(dict1)
        info_json = json.dumps(list1, ensure_ascii=False)
        return HttpResponse(info_json)


    else:
        all_lst = []
        page = request.GET.get('page', 1)
        gongdan_all_list = Gongdan.objects.filter(status=StatusName.objects.get(name="已收录")).order_by("-created_time")
        paginator = Paginator(gongdan_all_list, 10)
        page_of_gongdan = paginator.get_page(int(page))
        if int(page)>paginator.num_pages:
            return HttpResponse(json.dumps(all_lst, ensure_ascii=False))
        gongdan_lst = page_of_gongdan.object_list
        print(gongdan_lst)

        for gongdan in gongdan_lst:
            all_lst.append({
                'gongdanid': gongdan.gongdanid,
                'name':gongdan.name[0]+"同学",
                'excerpt': gongdan.excerpt,
                'reply': gongdan.reply,
                'status': gongdan.status.name,
                'created_time': str(gongdan.created_time).split('.')[0],
            })
        return HttpResponse(json.dumps(all_lst, ensure_ascii=False))
