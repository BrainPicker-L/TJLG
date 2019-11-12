from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import *
from user.models import Profile
from all_article.models import *
from datetime import datetime
import os
from Tjlg.settings import MEDIA_ROOT,BASE_DIR
from detail_article.models import DetailArticle
import json
from django.http import HttpResponse
from menuApi.models import Menu
from menuApi.forms import menuForm

from django.core.paginator import Paginator
import re
from django.views.decorators.csrf import csrf_exempt

from Tjlg.settings import HOSTS
from gradeList.models import *
from lectureApi.models import Lecture
from fuzzywuzzy import fuzz

def home(request):
    context = {}

    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def logout(request):
    context = {}
    auth.logout(request)
    return render(request, 'home.html', context)
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST or None,request.FILES or None)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            avatar = reg_form.cleaned_data['avatar']
            write_image(avatar)
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            user_profile = Profile(user=user,avatar=avatar)
            user_profile.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
def manage_article(request):
    context = {}
    author = request.user
    try:
        author = Profile.objects.filter(user=author)[0]
        context['articles'] =  TJLG_Article_Pyspider.objects.filter(author=author)
    except:
        context['articles'] = []
    return render(request, 'manage_article.html', context)



def write_image(myFile):
    if myFile == None:
        pass
    else:
        destination = open(os.path.join(MEDIA_ROOT+"/img", myFile.name), 'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

def edit_article(request, article_pk):
    context = {}
    if request.method == 'POST':
        article_form = ArticleForm(request.POST or None,request.FILES or None)
        if article_form.is_valid():
            article = TJLG_Article_Pyspider()
            article.author = Profile.objects.filter(user=request.user)[0]
            article.title = article_form.cleaned_data["title"]
            article.detail_url = article_form.cleaned_data["detail_url"]
            article.excerpt = article_form.cleaned_data["excerpt"]
            cur = datetime.now()
            article.created_time = "%s-%s-%s %s:%s"%(cur.year,cur.month,cur.day,cur.hour,cur.minute)
            article.last_updated_time = "%s-%s-%s %s:%s"%(cur.year,cur.month,cur.day,cur.hour,cur.minute)
            article.img1 = article_form.cleaned_data["img1"]
            article.img2 = article_form.cleaned_data["img2"]
            article.img3 = article_form.cleaned_data["img3"]
            article.img4 = article_form.cleaned_data["img4"]
            article.img5 = article_form.cleaned_data["img5"]
            article.img6 = article_form.cleaned_data["img6"]
            article.img7 = article_form.cleaned_data["img7"]
            article.img8 = article_form.cleaned_data["img8"]
            article.img9 = article_form.cleaned_data["img9"]
            write_image(article.img1)
            write_image(article.img2)
            write_image(article.img3)
            write_image(article.img4)
            write_image(article.img5)
            write_image(article.img6)
            write_image(article.img7)
            write_image(article.img8)
            write_image(article.img9)
            article.save()
            return redirect(request.GET.get('from', reverse('manage_article')))
    else:
        article_form = ArticleForm()
        context['article_form'] = article_form
        if str(article_pk) == "0":
            pass
        else:
            TJLG_Article_Pyspider.objects.get(pk=article_pk).delete()
    return render(request, 'edit_article.html', context)




def delete_article(request,article_pk):
    context = {}
    TJLG_Article_Pyspider.objects.get(pk=article_pk).delete()
    return redirect(request.GET.get('from', reverse('manage_article')))



def manage_detail(request):

    context = {}
    try:
        author = request.user
        author = Profile.objects.filter(user=author)[0]
        context['articles'] = DetailArticle.objects.filter(author=author)
    except:
        context['articles'] = []
    return render(request, 'manage_detail.html', context)


def edit_detail_article(request,article_pk):
    context = {}
    if request.method == 'POST':
        article_form = DetailArticleForm(request.POST or None, request.FILES or None)
        if article_form.is_valid():
            article = DetailArticle()
            article.author = Profile.objects.filter(user=request.user)[0]
            article.title = article_form.cleaned_data["title"]
            article.content = article_form.cleaned_data["content"]
            cur = datetime.now()
            article.created_time = "%s-%s-%s %s:%s"%(cur.year,cur.month,cur.day,cur.hour,cur.minute)
            article.last_updated_time = "%s-%s-%s %s:%s"%(cur.year,cur.month,cur.day,cur.hour,cur.minute)
            article.save()
            return redirect(request.GET.get('from', reverse('manage_detail')))

    else:
        article_form = DetailArticleForm()
        context['article_form'] = article_form
        if str(article_pk) == "0":
            pass
        else:
            DetailArticle.objects.get(pk=article_pk).delete()
    return render(request, 'edit_detail_article.html', context)


def delete_detail_article(request,article_pk):
    context = {}
    DetailArticle.objects.get(pk=article_pk).delete()
    return redirect(request.GET.get('from', reverse('manage_detail')))


def phone_detail_article(request,article_pk):
    context = {}
    context['article'] = DetailArticle.objects.get(pk=article_pk)
    return render(request, 'phone_detail_article.html', context)

def start_school_day(request):
    info_json = json.dumps({"start": "20190826"}, ensure_ascii=False)
    return HttpResponse(info_json)
def psf(request):
    info_json = json.dumps({"flag":"2019"})
    return HttpResponse(info_json)

def personal_flag(requset):
    info_json = json.dumps({"flag": "0"})
    return HttpResponse(info_json)


def lecture(request):
    querylist = Lecture.objects.all()
    info_list = []
    for i in querylist:
        #     list_display = ('headline', 'title', 'speaker', 'host','time','start_time','length','location','intro')
        dict1 = {}
        dict1['headline'] = i.headline
        dict1['title'] = i.title
        dict1['speaker'] = i.speaker
        dict1['host'] = i.host
        dict1['time'] = str(i.time).split(" ")[0]
        dict1['start_time'] = i.start_time
        dict1['length'] = i.length
        dict1['location'] = i.location
        dict1['intro'] = i.intro
        info_list.append(dict1)
    info_json = json.dumps(info_list, ensure_ascii=False)
    return HttpResponse(info_json)



def menu(request):
    if request.method == "GET":
        form = menuForm(request.GET)
        if form.is_valid():
            text_to_search = form.cleaned_data['menu_info']
            print(text_to_search)
            menu_all_list = Menu.objects.all()
            # menu_all_list = Menu.objects.filter(namePrice__contains=text_to_search)
            # if menu_all_list == 0:
            #     menu_all_list = Menu.objects.filter(diningRoom__contains=text_to_search)
            list1 = []
            for i in menu_all_list:
                value = fuzz.token_sort_ratio(text_to_search,i.namePrice)
                if value>=40:
                    dict1 = {}
                    dict1["diningRoom"] = i.diningRoom
                    dict1["winNum"] = i.winNum
                    dict1["namePrice"] = i.namePrice
                    dict1["value"] = value
                    list1.append(dict1)
            list1 = sorted(list1,key=lambda a:a['value'],reverse=True)
            info_json = json.dumps(list1, ensure_ascii=False)
            return HttpResponse(info_json)
    else:
        form = menuForm()
    return render(request, 'menu.html', {'form':form})


def menu_list(request):
    f = open('/home/TJLG/memu/memu.txt.utf8')

    menu_list = f.read().split("\n")

    all_list = []
    list1 = []
    list2 = []
    for i in menu_list:
        if "食堂" in i:
            if list1 != []:
                list1.append(list2)
                all_list.append(list1)
                list2 = []
            list1 = []
        elif "窗口" in i:
            if list2 != []:
                list1.append(list2)
            list2 = ["", []]
            list2[0] = i
        else:
            list2[1].append(i)
    list1.append(list2)
    all_list.append(list1)
    json_all_list = json.dumps(all_list, ensure_ascii=False)
    return HttpResponse(json_all_list)
    menu_all_list = Menu.objects.all()
    # menu_all_list = Menu.objects.filter(namePrice__contains=text_to_search)
    # if menu_all_list == 0:
    #     menu_all_list = Menu.objects.filter(diningRoom__contains=text_to_search)
    list1 = []
    for i in menu_all_list:
        value = fuzz.token_sort_ratio(text_to_search, i.namePrice)
        if value >= 40:
            dict1 = {}
            dict1["diningRoom"] = i.diningRoom
            dict1["winNum"] = i.winNum
            dict1["namePrice"] = i.namePrice
            dict1["value"] = value
            list1.append(dict1)
    list1 = sorted(list1, key=lambda a: a['value'], reverse=True)
    info_json = json.dumps(list1, ensure_ascii=False)
    return HttpResponse(info_json)

def guake(request):
    searchtext = request.GET.get("searchtext",'')
    if searchtext != '':
        guake_all_list = Guake.objects.all()
        list1 = []
        for i in guake_all_list:
            value = fuzz.token_sort_ratio(searchtext, i.Name)
            if value >= 20:
                dict1 = {}
                dict1["code"] = i.Code
                dict1["name"] = i.Name
                dict1["number"] = i.Number
                dict1["category"] = i.Category
                dict1["lost_rate"] = i.P0_59
                dict1["rate2"] =i.P60_69
                dict1["rate3"] =i.P70_79
                dict1["rate4"] =i.P80_89
                dict1["good_rate"] =i.P90_100
                dict1["value"] = value
                list1.append(dict1)
        list1 = sorted(list1, key=lambda a: a['value'], reverse=True)
        info_json = json.dumps(list1, ensure_ascii=False)
        return HttpResponse(info_json)

def email(request):
    page = request.GET.get('page', 1)
    emails_all_list = Email.objects.order_by("-create_time")
    paginator = Paginator(emails_all_list, 5)
    if int(page) <= paginator.num_pages:
        if page != '':
            context = {}
            page_of_emails = paginator.get_page(int(page))
            context['emails'] = page_of_emails.object_list
            context_list = []
            for i in context['emails']:
                dict1 = {}
                dict1["id"] = i.id
                dict1['title'] = i.title
                dict1['ask'] = i.ask
                dict1['answer'] = re.sub('\d+/\d+/\d+','',i.answer).replace('\r','')
                dict1['create_time'] = str(i.create_time).split(' ')[0]
                context_list.append(dict1)
            context_list_json = json.dumps(context_list, ensure_ascii=False)
            print(context_list_json)
            return HttpResponse(context_list_json)
    context_list = []
    context_list_json = json.dumps(context_list, ensure_ascii=False)
    return HttpResponse(context_list_json)

def emailSearch(request):
    searchtext = request.GET.get('searchtext', '')
    page = request.GET.get('page', '')
    emails_all_list = Email.objects.all()
    list1 = []

    for i in emails_all_list:
        value = fuzz.token_sort_ratio(searchtext, i.title)
        if value >= 80:
            dict1 = {}
            dict1["id"] = i.id
            dict1['title'] = i.title
            dict1['ask'] = i.ask
            dict1['answer'] = re.sub('\d+/\d+/\d+', '', i.answer).replace('\r', '')
            dict1['create_time'] = str(i.create_time).split(' ')[0]
            dict1["value"] = value
            list1.append(dict1)
    list1 = sorted(list1, key=lambda a: a['value'], reverse=True)[:20]
    info_json = json.dumps(list1, ensure_ascii=False)
    return HttpResponse(info_json)

def emaildetail(request):
    id = request.GET.get('id', '')
    try:
        if id != '':
            i = Email.objects.filter(id=int(id))[0]
            dict1 = {}
            dict1["id"] = i.id
            dict1['title'] = i.title
            dict1['ask'] = i.ask
            dict1['answer'] = re.sub('\d+/\d+/\d+', '', i.answer).replace('\r', '')
            dict1['create_time'] = str(i.create_time).split(' ')[0]
            info_json = json.dumps(dict1, ensure_ascii=False)
        else:
            info_json = json.dumps({}, ensure_ascii=False)
    except:
        info_json = json.dumps({}, ensure_ascii=False)
    return HttpResponse(info_json)

@csrf_exempt
def getarticle(request):
    try:
        articleObj = TJLG_Article_Pyspider()
        articleObj.author = Profile.objects.filter(user__username=request.POST.get('author',''))[0]
        articleObj.title = request.POST.get('title','')
        articleObj.detail_url = request.POST.get('detail_url','')
        articleObj.excerpt = request.POST.get('excerpt','')
        cur = datetime.now()
        articleObj.created_time = "%s-%s-%s %s:%s" % (cur.year, cur.month, cur.day, cur.hour, cur.minute)
        articleObj.last_updated_time = "%s-%s-%s %s:%s" % (cur.year, cur.month, cur.day, cur.hour, cur.minute)
        titlelist = gettitlelist()
        print(titlelist,articleObj.detail_url)
        if request.POST.get('title','') and articleObj.title and articleObj.excerpt and articleObj.title not in titlelist:
            articleObj.save()
            return HttpResponse(json.dumps({"insert":"success"},ensure_ascii=False))
        return HttpResponse(json.dumps({"insert": "Error,缺少字段或字段为空或数据重复"}, ensure_ascii=False))
    except:
        return HttpResponse(json.dumps({"insert": "未知错误，联系子哲"}, ensure_ascii=False))


def gettitlelist():
    titlelist = []
    articles = TJLG_Article_Pyspider.objects.all()
    for article in articles:
        titlelist.append(article.title)
    return titlelist

from ZFCheckCode.pj import AhuPj
@csrf_exempt
def jspj(request):
    user = request.POST.get('user', '')
    password = request.POST.get('password', '')
    print(user,password)
    a = AhuPj(user,password)
    data = a.run()
    return HttpResponse(json.dumps({"pjFlag": data}, ensure_ascii=False))


def sort_time(time, create_time):
    h_m = str(create_time.strftime("%H:%M"))
    month_num = time // 30
    if month_num == 0:
        if time == 0:
            time_text = "今天 %s" % h_m
        elif time == 1:
            time_text = "昨天 %s" % h_m
        elif time == 2:
            time_text = "前天 %s" % h_m
        elif 0 < time <= 30:
            time_text = "%d天前 %s" % (time, h_m)
    elif month_num > 0:
        time_text = "%d月前 %s" % (month_num, h_m)
    else:
        time_text = "未来 %s" % h_m
    return time_text





def school_life(request):
    info_list = []
    for i in SchoolLife.objects.all().order_by('-id'):
        dict1 = {}
        dict1["author"] = i.author_name
        dict1["avatar"] = HOSTS +i.avatar.url
        dict1["weixin_link"] = i.weixin_link
        dict1["background_img"] = HOSTS +i.background_img.url
        info_list.append(dict1)
    return HttpResponse(json.dumps(info_list, ensure_ascii=False))

def TJLG_school_life(request):
    info_list = []
    for i in SchoolLife_TJLG.objects.all().order_by('-id'):
        dict1 = {}
        dict1["author"] = i.author_name
        dict1["avatar"] = HOSTS +i.avatar.url
        dict1["weixin_link"] = i.weixin_link
        dict1["background_img"] = HOSTS +i.background_img.url
        info_list.append(dict1)
    return HttpResponse(json.dumps(info_list, ensure_ascii=False))

def ahu_advert(request):
    info_list = []
    for i in AhuAdvert.objects.all().order_by('-id'):
        dict1 = {}
        dict1["weixin_link"] = i.weixin_link
        dict1["background_img"] = HOSTS +i.background_img.url
        info_list.append(dict1)
    return HttpResponse(json.dumps(info_list, ensure_ascii=False))


def tjlg_advert(request):
    info_list = []
    for i in TJLGAdvert.objects.all().order_by('-id'):
        dict1 = {}
        dict1["weixin_link"] = i.weixin_link
        dict1["background_img"] = HOSTS +i.background_img.url
        info_list.append(dict1)
    return HttpResponse(json.dumps(info_list, ensure_ascii=False))



def get_class_info(request):
    search_text = request.GET.get('search_text', '')
    page = request.GET.get('page', 0)
    class_all_list = ClassInfo.objects.filter(kcmc__icontains=search_text)
    paginator = Paginator(class_all_list, 10)
    if int(page) <= paginator.num_pages:
        if page != '':
            context_list = []
            page_of_class = paginator.get_page(int(page))
            classes = page_of_class.object_list
            for i in classes:
                dct = {}
                dct['kcmc'] = i.kcmc
                dct['ls'] = i.ls
                dct['kcdd'] = i.kcdd
                dct['xqj'] = i.xqj
                dct['skjc'] = i.skjc
                dct['skcd'] = i.skcd
                dct['qszs'] = i.qszs
                dct['jszs'] = i.jszs
                dct['dsz'] = i.dsz
                dct['extra'] = i.extra
                context_list.append(dct)
            return HttpResponse(json.dumps(context_list, ensure_ascii=False))

    else:
        context_list = []
        context_list_json = json.dumps(context_list)
        return HttpResponse(context_list_json)
