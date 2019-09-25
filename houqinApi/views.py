from django.shortcuts import render

# Create your views here.
from .models import *
from .forms import *

def houqin_home(request):
    context = {}
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


