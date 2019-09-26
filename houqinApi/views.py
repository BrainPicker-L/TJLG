from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import *
import time
from .forms import *
from django.http import HttpResponse
import random
import json

def houqin_home(request):
    context = {}
    if request.user.username == "后勤服务中心":

        context["select_form"] = SelectForm()
        if request.method == "GET":
            status = request.GET.get('status','未处理')
            context["status_now"] = status
        elif request.method == "POST":
            repair_man_pk = request.POST.get("sel_value", RepairMan.objects.get(name="无").pk)
            status_pk = request.POST.get("sel_value2", StatusName.objects.get(name="未处理").pk)
            gd_pk = request.POST.get("gd_pk", '')
            status = request.POST.get("status", '未处理')
            context["status_now"] = status
            obj = Gongdan.objects.get(pk=gd_pk)
            print(repair_man_pk)
            obj.repair_man = RepairMan.objects.get(pk=repair_man_pk)
            print(obj.repair_man)
            obj.status = StatusName.objects.get(pk=status_pk)
            print(obj.status)
            obj.save()
        if status == "未处理":
            context["gongdans"] = Gongdan.objects.filter(status__name="未处理").order_by('-created_time')

        elif status == "已处理":
            context["gongdans"] = Gongdan.objects.filter(status__name="已处理").order_by('-created_time')

        elif status == "维修完成":
            context["gongdans"] = Gongdan.objects.filter(status__name="维修完成").order_by('-created_time')

    return render(request, 'houqin_home.html', context)



def houqin_detail(request,gd_pk):   #传入参数工单pk
    context={}
    context["gongdan"] = Gongdan.objects.get(id=int(gd_pk))
    print(gd_pk)
    return render(request, 'houqin_detail.html', context)



@csrf_exempt
def add_gongdan(request):
    sno = request.POST.get('sno','')
    name = request.POST.get('name','')
    phonenum = request.POST.get('phonenum','')
    pos = request.POST.get('pos','')
    abletime = request.POST.get('abletime','')
    excerpt = request.POST.get('excerpt','')
    if not (sno and name and phonenum and pos and abletime and excerpt):
        return HttpResponse(json.dumps({"error":"所有字段不能为空"}, ensure_ascii=False))
    obj = Gongdan()
    obj.gongdanid = time.strftime("%Y%m%d")+sno+str(random.randint(1,1000)).zfill(4)
    obj.sno = sno
    obj.name = name
    obj.phonenum = phonenum
    obj.pos = pos
    obj.abletime = abletime
    obj.excerpt = excerpt
    obj.repair_man = RepairMan.objects.get(name="无")
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
            'repair_man_name': gongdan.repair_man.name,
        'repair_man_phonenum':gongdan.repair_man.phonenum,
        'status':gongdan.status.name,
        'created_time':str(gongdan.created_time).split('.')[0],
        })
    return HttpResponse(json.dumps(all_lst, ensure_ascii=False))
