from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import *
from user.models import Profile
from all_article.models import Article
import datetime
import os
from Tjlg.settings import MEDIA_ROOT
from detail_article.models import DetailArticle
import json
from django.http import HttpResponse
from menuApi.models import Menu
from menuApi.forms import menuForm
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
    author = Profile.objects.filter(user=author)[0]
    context['articles'] =  Article.objects.filter(author=author)
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
            article = Article()
            article.author = Profile.objects.filter(user=request.user)[0]
            article.title = article_form.cleaned_data["title"]
            article.detail_url = article_form.cleaned_data["detail_url"]
            article.excerpt = article_form.cleaned_data["excerpt"]
            cur = datetime.datetime.now()
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
            Article.objects.get(pk=article_pk).delete()
    return render(request, 'edit_article.html', context)




def delete_article(request,article_pk):
    context = {}
    Article.objects.get(pk=article_pk).delete()
    return redirect(request.GET.get('from', reverse('manage_article')))



def manage_detail(request):
    context = {}
    author = request.user
    author = Profile.objects.filter(user=author)[0]
    context['articles'] = DetailArticle.objects.filter(author=author)
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
            cur = datetime.datetime.now()
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
    info_json = json.dumps({"start": "20190225"}, ensure_ascii=False)
    return HttpResponse(info_json)

from lectureApi.models import Lecture
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
            menu_all_list = Menu.objects.filter(namePrice__contains=text_to_search)
            if menu_all_list == 0:
                menu_all_list = Menu.objects.filter(diningRoom__contains=text_to_search)
            list1 = []
            for i in menu_all_list:
                dict1 = {}
                dict1["diningRoom"] = i.diningRoom
                dict1["winNum"] = i.winNum
                dict1["namePrice"] = i.namePrice
                list1.append(dict1)
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