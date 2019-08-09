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
from gradeList.models import Guake
from django.core.paginator import Paginator
import re
from django.views.decorators.csrf import csrf_exempt
import time
import requests
from Tjlg.settings import HOSTS

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
    info_json = json.dumps({"start": "20190225"}, ensure_ascii=False)
    return HttpResponse(info_json)
def psf(request):
    info_json = json.dumps({"flag":"2019"})
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

from fuzzywuzzy import fuzz

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
        articleObj = Article()
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
    except Exception as e:
        return HttpResponse(json.dumps({"insert": e}, ensure_ascii=False))


def gettitlelist():
    titlelist = []
    articles = Article.objects.all()
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




@csrf_exempt
def useraction(request):
    if request.method == "POST":
        try:
            Sno = request.POST.get('OnsUha','')
            userAvatar = request.POST.get('userAvatar','')
            excerpt = request.POST.get('excerpt','')
            img = request.POST.get('img','')
            print(Sno,userAvatar,excerpt,img)
            print(img)
            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/'+Sno+'.gif'

            img_file_path = 'action_img/'+Sno+'_'+str(time.time())+'.gif'

            if userAvatar!='' and excerpt != '' and Sno != '':#"20" in Sno and len(Sno)<12 and userAvatar!='':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno,userAvatar=avatar_file_path)
                article_obj = UserAction()
                article_obj.author = user_obj
                article_obj.excerpt = excerpt
                if img!='':
                    with open(media_path + img_file_path, 'wb') as f:
                        r = requests.get(url=img)
                        f.write(r.content)
                    f.close()
                    article_obj.img = img_file_path
                article_obj.save()
                return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({"status": '没有传头像'}, ensure_ascii=False))
        except Exception as e:
            return HttpResponse(json.dumps({"status": e}, ensure_ascii=False))
    elif request.method == "GET":
        page = request.GET.get('page', 0)
        actions_all_list = UserAction.objects.order_by("-created_time")
        paginator = Paginator(actions_all_list, 7)
        time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        if int(page) <= paginator.num_pages:
            if page != '':
                context_list = []
                page_of_actions = paginator.get_page(int(page))
                actions = page_of_actions.object_list

                for action in actions:
                    context = {}
                    context['author_id'] = action.author.pk
                    context['action_id'] = action.pk
                    context['author'] = action.author.Sno
                    context['avatar'] = HOSTS + action.author.userAvatar.url
                    context['excerpt'] = action.excerpt
                    context['like_num'] = action.like_num
                    context['like_users'] = [i.user.Sno for i in UserActionLike.objects.filter(action_id=action.pk)]
                    if str(action.img) != '':
                        context['img'] = HOSTS + action.img.url
                    else:
                        context['img'] = ''
                    context['commit_count'] = ArticleComment.objects.filter(article_id=action.id).count()
                    time2 = datetime(action.created_time.year, action.created_time.month, action.created_time.day)
                    context['time'] = sort_time((time1 - time2).days, action.created_time)
                    context_list.append(context)
                context_list_json = json.dumps(context_list)
                print(context_list_json)
                return HttpResponse(context_list_json)
            else:
                context_list = []
                context_list_json = json.dumps(context_list)
                return HttpResponse(context_list_json)
        else:
            context_list = []
            context_list_json = json.dumps(context_list)
            return HttpResponse(context_list_json)


@csrf_exempt
def comment_action(request):
    if request.method == "POST":
        try:
            Sno = request.POST.get('OnsUha','')
            userAvatar = request.POST.get('userAvatar', '')
            content = request.POST.get('content','')
            action_id = int(request.POST.get('action_id',1))


            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'


            if Sno != '' and content != '' and action_id!='' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno, userAvatar=avatar_file_path)
                comment = ArticleComment()
                article_obj = UserAction.objects.get(pk=action_id)
                comment.article = article_obj
                comment.user = user_obj
                comment.content = content
                comment.save()
                return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({"status": 'post中有值为空'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲'}, ensure_ascii=False))
    elif request.method == "GET":
        action_id = request.GET.get('action_id','')

        if action_id != '':
            try:
                comments = ArticleComment.objects.filter(article_id=action_id)
                context_dict = {}
                context_list = []
                time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
                for comment in comments:
                    context = {}
                    context['action_id'] = comment.article.pk
                    context['commit_id'] = comment.pk
                    context["author_id"] = comment.user.pk
                    context['author'] = comment.user.Sno
                    context['avatar'] = HOSTS +comment.user.userAvatar.url
                    context['commit_content'] = comment.content
                    context['like_num'] = comment.like_num


                    time2 = datetime(comment.create_time.year, comment.create_time.month, comment.create_time.day)
                    context['time'] = sort_time((time1 - time2).days, comment.create_time)
                    context_list.append(context)
                action_obj = UserAction.objects.filter(id=action_id)[0]
                context_dict['context_list'] = context_list
                context_dict['action_author_id'] = action_obj.author.pk
                context_dict['action_author'] = action_obj.author.Sno
                context_dict['action_author_avatar'] = HOSTS + action_obj.author.userAvatar.url
                context_dict['action_excerpt'] = action_obj.excerpt
                context_dict['like_num'] = action_obj.like_num
                if str(comment.article.img) != '':
                    context_dict['img'] = HOSTS + action_obj.img.url
                else:
                    context_dict['img'] = ''
                context_dict_json = json.dumps(context_dict)
                return HttpResponse(context_dict_json)
            except:
                context_dict = {}
                context_dict_json = json.dumps(context_dict)
                return HttpResponse(context_dict_json)
        else:
            context_dict = {}
            context_dict_json = json.dumps(context_dict)
            return HttpResponse(context_dict_json)

    else:
        return HttpResponse(json.dumps({"status": 'action_id不能为空'}, ensure_ascii=False))


def personal_action(request):
    if request.method == "GET":
        author_id = request.GET.get('author_id','')
        if author_id != '':
            personal_actions = UserAction.objects.filter(author_id=author_id).order_by("-created_time")
            context_dict = {}
            context_list = []
            time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
            for personal_action in personal_actions:
                context = {}
                context['author_id'] = personal_action.author.pk
                context['action_id'] = personal_action.pk
                context['author'] = personal_action.author.Sno
                context['avatar'] = HOSTS + personal_action.author.userAvatar.url
                context['excerpt'] = personal_action.excerpt
                context['like_num'] = personal_action.like_num
                context['like_users'] = [i.user.Sno for i in UserActionLike.objects.filter(action_id=personal_action.pk)]
                if str(personal_action.img) != '':
                    context['img'] = HOSTS + personal_action.img.url
                else:
                    context['img'] = ''
                context['commit_count'] = ArticleComment.objects.filter(article_id=personal_action.id).count()
                time2 = datetime(personal_action.created_time.year, personal_action.created_time.month, personal_action.created_time.day)
                context['time'] = sort_time((time1 - time2).days, personal_action.created_time)
                context_list.append(context)
            author_obj = ahuUser.objects.filter(id=author_id)[0]
            context_dict['context_list'] = context_list
            context_dict['author'] = author_obj.Sno
            context_dict['avatar'] = HOSTS + author_obj.userAvatar.url

            context_dict_json = json.dumps(context_dict)
            return HttpResponse(context_dict_json)
        else:
            context_dict = {}
            context_dict_json = json.dumps(context_dict)
            return HttpResponse(context_dict_json)
    else:
        return HttpResponse(json.dumps({"status": 'fail'}, ensure_ascii=False))


@csrf_exempt
def change_like_num_action(request):
    if request.method == "POST":
        try:
            Sno = request.POST.get('OnsUha', '')
            userAvatar = request.POST.get('userAvatar', '')
            action_id = int(request.POST.get('action_id', 1))



            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            if Sno != '' and action_id != '' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno, userAvatar=avatar_file_path)
                action_obj = UserAction.objects.get(pk=action_id)
                like_num,like_num_created = UserActionLike.objects.get_or_create(user=user_obj, action=action_obj)
                if like_num_created == True:
                    action_obj.like_num += 1
                else:
                    action_obj.like_num -= 1
                    UserActionLike.objects.get(user=user_obj, action=action_obj).delete()
                action_obj.save()
                return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))

            else:
                return HttpResponse(json.dumps({"status": 'post中有值为空'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲,查看action_id是否不存在'}, ensure_ascii=False))

@csrf_exempt
def change_like_num_comment(request):
    if request.method == "POST":
        try:
            Sno = request.POST.get('OnsUha', '')
            userAvatar = request.POST.get('userAvatar', '')
            comment_id = int(request.POST.get('comment_id', 1))

            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            if Sno != '' and comment_id != '' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                comment_obj = ArticleComment.objects.get(pk=comment_id)
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno, userAvatar=avatar_file_path)
                like_num, like_num_created = UserCommentLike.objects.get_or_create(user=user_obj, comment=comment_obj)
                if like_num_created == True:
                    comment_obj.like_num += 1
                else:
                    comment_obj.like_num -= 1
                    UserCommentLike.objects.get(user=user_obj, comment=comment_obj).delete()
                comment_obj.save()
                return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({"status": 'post中有值为空'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲,查看comment_id是否不存在'}, ensure_ascii=False))


def hip_test_api(request):
    list1 = [{'学年': '2016-2017', '学期': '1', '总绩点': 0, '学期绩点': 0, '学年绩点': 0, '成绩列表': [{'学年': '2016-2017', '学期': '1', '课程代码': '03010010', '课程名称': '大学计算机基础', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   3.00', '平时成绩': '97', '期中成绩': '', '期末成绩': '73', '实验成绩': '', '成绩': '80', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '信息工程学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '06030010', '课程名称': '英语一级', '课程性质': '公共必修课', '课程归属': '', '学分': '4.0', '绩点': '   1.00', '平时成绩': '85', '期中成绩': '', '期末成绩': '37', '实验成绩': '', '成绩': '61', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '外语学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '07010010', '课程名称': '土木工程概论', '课程性质': '专业基础必修课', '课程归属': '', '学分': '1.5', '绩点': '   2.00', '平时成绩': '70', '期中成绩': '', '期末成绩': '70', '实验成绩': '', '成绩': '70', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '07010020', '课程名称': '土木工程制图(上)', '课程性质': '专业基础必修课', '课程归属': '', '学分': '2.5', '绩点': '   1.00', '平时成绩': '70', '期中成绩': '', '期末成绩': '55', '实验成绩': '', '成绩': '60', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '10010030', '课程名称': '思想品德修养及法律基础', '课程性质': '公共必修课', '课程归属': '', '学分': '3.0', '绩点': '   3.00', '平时成绩': '69', '期中成绩': '', '期末成绩': '93', '实验成绩': '', '成绩': '82', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '11010010', '课程名称': '高等数学I（上）', '课程性质': '公共必修课', '课程归属': '', '学分': '4.5', '绩点': '   2.00', '平时成绩': '100', '期中成绩': '', '期末成绩': '62', '实验成绩': '', '成绩': '73', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '13010090', '课程名称': '大学体育（一）', '课程性质': '公共必修课', '课程归属': '', '学分': '1.0', '绩点': '   2.00', '平时成绩': '100', '期中成绩': '', '期末成绩': '65', '实验成绩': '', '成绩': '79', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '体育教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '15011010', '课程名称': '军训', '课程性质': '实践课', '课程归属': '', '学分': '2.0', '绩点': '   4.00', '平时成绩': '优秀', '期中成绩': '', '期末成绩': '优秀', '实验成绩': '', '成绩': '优秀', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '军事理论教研室', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '37010010', '课程名称': '军事理论及训练', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   3.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '良好', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '军事理论教研室', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '38010010', '课程名称': '大学生就业指导I', '课程性质': '公共选修课', '课程归属': '', '学分': '0.5', '绩点': '   2.00', '平时成绩': '75', '期中成绩': '', '期末成绩': '78', '实验成绩': '', '成绩': '77', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '就业办公室', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '1', '课程代码': '38020010', '课程名称': '健康教育', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   3.00', '平时成绩': '86', '期中成绩': '', '期末成绩': '79', '实验成绩': '', '成绩': '83', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '德育教研室', '备注': '', '重修标记': ''}]}, {'学年': '2016-2017', '学期': '2', '总绩点': 0, '学期绩点': 0, '学年绩点': 0, '成绩列表': [{'学年': '2016-2017', '学期': '2', '课程代码': '008', '课程名称': '排球', '课程性质': '公共基础课', '课程归属': '', '学分': '1.0', '绩点': '   4.00', '平时成绩': '100', '期中成绩': '', '期末成绩': '90', '实验成绩': '', '成绩': '94', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '03010340', '课程名称': '计算机程序设计（VB）', '课程性质': '公共必修课', '课程归属': '', '学分': '4.0', '绩点': '   3.00', '平时成绩': '92', '期中成绩': '', '期末成绩': '88', '实验成绩': '', '成绩': '89', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '信息工程学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '06030011', '课程名称': '英语二级', '课程性质': '公共必修课', '课程归属': '', '学分': '4.0', '绩点': '   1.00', '平时成绩': '86', '期中成绩': '', '期末成绩': '44', '实验成绩': '', '成绩': '65', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '外语学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '07020020', '课程名称': '土木工程制图(下)', '课程性质': '专业必修课', '课程归属': '', '学分': '2.5', '绩点': '   2.00', '平时成绩': '75', '期中成绩': '', '期末成绩': '78', '实验成绩': '', '成绩': '77', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '07020030', '课程名称': '理论力学', '课程性质': '专业基础必修课', '课程归属': '', '学分': '3.0', '绩点': '', '平时成绩': '88', '期中成绩': '', '期末成绩': '41', '实验成绩': '', '成绩': '55', '辅修标记': '0', '补考成绩': '51', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '10010010', '课程名称': '马克思主义基本原理概论', '课程性质': '公共必修课', '课程归属': '', '学分': '3.0', '绩点': '', '平时成绩': '86', '期中成绩': '', '期末成绩': '45', '实验成绩': '', '成绩': '57', '辅修标记': '0', '补考成绩': '0', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '11010011', '课程名称': '高等数学I（下）', '课程性质': '公共必修课', '课程归属': '', '学分': '5.0', '绩点': '   1.00', '平时成绩': '90', '期中成绩': '', '期末成绩': '52', '实验成绩': '', '成绩': '63', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '11020010', '课程名称': '大学物理(上）', '课程性质': '公共基础课', '课程归属': '', '学分': '3.0', '绩点': '   2.00', '平时成绩': '90', '期中成绩': '', '期末成绩': '56', '实验成绩': '83', '成绩': '72', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '11021010', '课程名称': '大学物理实验（上）', '课程性质': '实践课', '课程归属': '', '学分': '1.0', '绩点': '   1.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '及格', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '17010010', '课程名称': '文献检索', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   2.00', '平时成绩': '92', '期中成绩': '', '期末成绩': '57.5', '实验成绩': '', '成绩': '78', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '图书馆', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '24010011', '课程名称': '创新教育', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   2.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '中等', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '创新创业发展中心', '备注': '', '重修标记': ''}, {'学年': '2016-2017', '学期': '2', '课程代码': '38010050', '课程名称': '口才艺术与社交礼仪', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   4.00', '平时成绩': '98', '期中成绩': '', '期末成绩': '98.7', '实验成绩': '', '成绩': '98', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '德育教研室', '备注': '', '重修标记': ''}]}, {'学年': '2017-2018', '学期': '1', '总绩点': 0, '学期绩点': 0, '学年绩点': 0, '成绩列表': [{'学年': '2017-2018', '学期': '1', '课程代码': '008', '课程名称': '排球', '课程性质': '公共基础课', '课程归属': '', '学分': '1.0', '绩点': '   3.00', '平时成绩': '100', '期中成绩': '', '期末成绩': '80', '实验成绩': '', '成绩': '88', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '06030012', '课程名称': '英语三级', '课程性质': '公共必修课', '课程归属': '', '学分': '3.0', '绩点': '   1.00', '平时成绩': '80', '期中成绩': '', '期末成绩': '57', '实验成绩': '', '成绩': '69', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '外语学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '07010040', '课程名称': '材料力学', '课程性质': '专业基础必修课', '课程归属': '', '学分': '3.0', '绩点': '   1.00', '平时成绩': '70', '期中成绩': '', '期末成绩': '35', '实验成绩': '', '成绩': '46', '辅修标记': '0', '补考成绩': '65', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '07010050', '课程名称': '工程地质', '课程性质': '专业基础必修课', '课程归属': '', '学分': '1.5', '绩点': '   1.00', '平时成绩': '86', '期中成绩': '', '期末成绩': '42', '实验成绩': '', '成绩': '64', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '07010060', '课程名称': '测量学', '课程性质': '专业必修课', '课程归属': '', '学分': '3.0', '绩点': '   2.00', '平时成绩': '83', '期中成绩': '', '期末成绩': '66', '实验成绩': '', '成绩': '71', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '07011010', '课程名称': '识图训练', '课程性质': '实践课', '课程归属': '', '学分': '1.0', '绩点': '   2.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '中等', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '07011020', '课程名称': '测量实习', '课程性质': '实践课', '课程归属': '', '学分': '2.0', '绩点': '   1.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '及格', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '10010040', '课程名称': '中国近代史纲要', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   2.00', '平时成绩': '60', '期中成绩': '', '期末成绩': '82', '实验成绩': '', '成绩': '75', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '11010021', '课程名称': '线性代数I', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   1.00', '平时成绩': '70', '期中成绩': '', '期末成绩': '57', '实验成绩': '', '成绩': '64', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '11020011', '课程名称': '大学物理(下）', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   2.00', '平时成绩': '100', '期中成绩': '', '期末成绩': '57', '实验成绩': '78', '成绩': '74', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '11021011', '课程名称': '大学物理实验（下）', '课程性质': '实践课', '课程归属': '', '学分': '1.0', '绩点': '   1.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '不及格', '辅修标记': '0', '补考成绩': '及格', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '24010012', '课程名称': '创业教育', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   4.00', '平时成绩': '80', '期中成绩': '', '期末成绩': '100', '实验成绩': '', '成绩': '92', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '创新创业发展中心', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '1', '课程代码': '25010011', '课程名称': '大学生职业生涯规划', '课程性质': '公共选修课', '课程归属': '', '学分': '0.5', '绩点': '   2.00', '平时成绩': '62', '期中成绩': '', '期末成绩': '82', '实验成绩': '', '成绩': '72', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '就业办公室', '备注': '', '重修标记': ''}]}, {'学年': '2017-2018', '学期': '2', '总绩点': 0, '学期绩点': 0, '学年绩点': 0, '成绩列表': [{'学年': '2017-2018', '学期': '2', '课程代码': '008', '课程名称': '排球', '课程性质': '公共基础课', '课程归属': '', '学分': '1.0', '绩点': '   4.00', '平时成绩': '80', '期中成绩': '', '期末成绩': '99', '实验成绩': '', '成绩': '91', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '06030013', '课程名称': '英语四级', '课程性质': '公共必修课', '课程归属': '', '学分': '3.0', '绩点': '   2.00', '平时成绩': '92', '期中成绩': '', '期末成绩': '62', '实验成绩': '', '成绩': '77', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '外语学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '07010070', '课程名称': '结构力学', '课程性质': '专业基础必修课', '课程归属': '', '学分': '4.0', '绩点': '   1.00', '平时成绩': '90', '期中成绩': '', '期末成绩': '58', '实验成绩': '', '成绩': '68', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '07010120', '课程名称': '建筑设备工程', '课程性质': '专业基础限选课', '课程归属': '', '学分': '2.0', '绩点': '   1.00', '平时成绩': '78', '期中成绩': '', '期末成绩': '54', '实验成绩': '', '成绩': '66', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '07011030', '课程名称': '认识实习', '课程性质': '实践课', '课程归属': '', '学分': '1.0', '绩点': '   1.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '及格', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '07011040', '课程名称': '土木工程材料集中训练', '课程性质': '实践课', '课程归属': '', '学分': '2.0', '绩点': '', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '不及格', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '07020030', '课程名称': '理论力学', '课程性质': '专业基础必修课', '课程归属': '', '学分': '3.0', '绩点': '   2.00', '平时成绩': '96', '期中成绩': '', '期末成绩': '64', '实验成绩': '', '成绩': '74', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': '重修'}, {'学年': '2017-2018', '学期': '2', '课程代码': '07020050', '课程名称': '土木工程CAD', '课程性质': '专业基础限选课', '课程归属': '', '学分': '2.0', '绩点': '   2.00', '平时成绩': '70', '期中成绩': '', '期末成绩': '75', '实验成绩': '', '成绩': '73', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '07020060', '课程名称': '土木工程材料', '课程性质': '专业基础必修课', '课程归属': '', '学分': '3.0', '绩点': '', '平时成绩': '70', '期中成绩': '', '期末成绩': '17', '实验成绩': '', '成绩': '33', '辅修标记': '0', '补考成绩': '45', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '10010010', '课程名称': '马克思主义基本原理概论', '课程性质': '公共必修课', '课程归属': '', '学分': '3.0', '绩点': '   1.00', '平时成绩': '85', '期中成绩': '', '期末成绩': '62', '实验成绩': '', '成绩': '69', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': '重修'}, {'学年': '2017-2018', '学期': '2', '课程代码': '10010020', '课程名称': '毛泽东思想和中国特色社会主义理论体系概论', '课程性质': '公共必修课', '课程归属': '', '学分': '5.0', '绩点': '   3.00', '平时成绩': '85', '期中成绩': '', '期末成绩': '84', '实验成绩': '', '成绩': '84', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '11010031', '课程名称': '概率论与数理统计I', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   3.00', '平时成绩': '86', '期中成绩': '', '期末成绩': '86', '实验成绩': '', '成绩': '86', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '数理教研部', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '24010030', '课程名称': '弟子规与人生修养', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   4.00', '平时成绩': '', '期中成绩': '', '期末成绩': '100', '实验成绩': '', '成绩': '优秀', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '德育教研室', '备注': '', '重修标记': ''}, {'学年': '2017-2018', '学期': '2', '课程代码': '24010040', '课程名称': '艺术与审美', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   4.00', '平时成绩': '', '期中成绩': '', '期末成绩': '100', '实验成绩': '', '成绩': '优秀', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '教务处', '备注': '', '重修标记': ''}]}, {'学年': '2018-2019', '学期': '1', '总绩点': 0, '学期绩点': 0, '学年绩点': 0, '成绩列表': [{'学年': '2018-2019', '学期': '1', '课程代码': '07010100', '课程名称': '房屋建筑学', '课程性质': '专业基础限选课', '课程归属': '', '学分': '4.0', '绩点': '   1.00', '平时成绩': '90', '期中成绩': '', '期末成绩': '49', '实验成绩': '', '成绩': '61', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07010110', '课程名称': '钢筋混凝土结构设计原理', '课程性质': '专业限选课', '课程归属': '', '学分': '3.0', '绩点': '   3.00', '平时成绩': '80', '期中成绩': '', '期末成绩': '81', '实验成绩': '', '成绩': '81', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07010140', '课程名称': '工程经济', '课程性质': '专业基础限选课', '课程归属': '', '学分': '3.0', '绩点': '   1.00', '平时成绩': '55', '期中成绩': '', '期末成绩': '50', '实验成绩': '', '成绩': '52', '辅修标记': '0', '补考成绩': '60', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07010152', '课程名称': '建工专业英语', '课程性质': '专业基础限选课', '课程归属': '', '学分': '2.0', '绩点': '   1.00', '平时成绩': '85', '期中成绩': '', '期末成绩': '39', '实验成绩': '', '成绩': '62', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07010210', '课程名称': '建筑项目管理', '课程性质': '专业限选课', '课程归属': '', '学分': '2.5', '绩点': '   1.00', '平时成绩': '79', '期中成绩': '', '期末成绩': '54', '实验成绩': '', '成绩': '62', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07011040', '课程名称': '土木工程材料集中训练', '课程性质': '实践课', '课程归属': '', '学分': '2.0', '绩点': '   1.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '及格', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': '重修'}, {'学年': '2018-2019', '学期': '1', '课程代码': '07011050', '课程名称': '工程结构创新实践', '课程性质': '实践课', '课程归属': '', '学分': '1.0', '绩点': '   2.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '中等', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07011061', '课程名称': '房屋建筑课程设计', '课程性质': '实践课', '课程归属': '', '学分': '2.0', '绩点': '   1.00', '平时成绩': '', '期中成绩': '', '期末成绩': '', '实验成绩': '', '成绩': '及格', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '07020060', '课程名称': '土木工程材料', '课程性质': '专业基础必修课', '课程归属': '', '学分': '3.0', '绩点': '   2.00', '平时成绩': '90', '期中成绩': '', '期末成绩': '70', '实验成绩': '', '成绩': '76', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '土木工程学院', '备注': '', '重修标记': '重修'}, {'学年': '2018-2019', '学期': '1', '课程代码': '10010051', '课程名称': '大学语文（应用文写作）', '课程性质': '公共必修课', '课程归属': '', '学分': '2.0', '绩点': '   2.00', '平时成绩': '77', '期中成绩': '', '期末成绩': '76', '实验成绩': '', '成绩': '77', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': ''}, {'学年': '2018-2019', '学期': '1', '课程代码': '10010060', '课程名称': '形势与政策', '课程性质': '公共选修课', '课程归属': '', '学分': '1.0', '绩点': '   3.00', '平时成绩': '80', '期中成绩': '', '期末成绩': '83', '实验成绩': '', '成绩': '82', '辅修标记': '0', '补考成绩': '', '重修成绩': '', '开课学院': '思想政治教育教研部', '备注': '', '重修标记': ''}]}]

    return HttpResponse(json.dumps(list1, ensure_ascii=False))



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
