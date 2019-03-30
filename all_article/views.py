from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator
from django.conf import settings
import json
from django.http import HttpResponse
from datetime import datetime
from Tjlg.settings import HOSTS
def sort_time(time,create_time):
    h_m = str(create_time.strftime("%H:%M"))
    month_num = time//30
    if month_num==0:
        if time == 0:
            time_text = "今天 %s"%h_m
        elif time == 1:
            time_text = "昨天 %s"%h_m
        elif time == 2:
            time_text = "前天 %s"%h_m
        elif 0<time<=30:
            time_text = "%d天前 %s"%(time,h_m)
    elif month_num>0:
        time_text = "%d月前 %s"%(month_num,h_m)
    else:
        time_text = "未来 %s" %h_m
    return time_text




def article_list(request):
    page = request.GET.get('page','')
    articles_all_list = Article.objects.order_by("-created_time")
    paginator = Paginator(articles_all_list, 5)
    if int(page) <= paginator.num_pages:
        if page!= '':
            context = {}
            page_of_articles = paginator.get_page(int(page))
            print(page,paginator.num_pages)
            context['articles'] = page_of_articles.object_list
            context_list = []
            time1 = datetime(datetime.now().year,datetime.now().month,datetime.now().day)
            for i in context['articles']:
                dict1 = {}
                dict1['author'] = str(i.author)
                dict1['avatar'] = HOSTS+i.author.avatar.url
                dict1['title'] = i.title
                time2 = datetime(i.created_time.year,i.created_time.month,i.created_time.day)
                dict1['time'] = sort_time((time1-time2).days, i.created_time)
                dict1['excerpt'] = i.excerpt
                if i.detail_url == "":
                    dict1['detail'] = None
                else:
                    dict1['detail'] = i.detail_url
                dict1['author_detail'] = ""
                dict1['image'] = []
                if str(i.img1) != "":
                    dict1['image'].append(HOSTS + i.img1.url)
                if str(i.img2) != "":
                    dict1['image'].append(HOSTS + i.img2.url)
                if str(i.img3) != "":
                    dict1['image'].append(HOSTS + i.img3.url)
                if str(i.img4) != "":
                    dict1['image'].append(HOSTS + i.img4.url)
                if str(i.img5) != "":
                    dict1['image'].append(HOSTS + i.img5.url)
                if str(i.img6) != "":
                    dict1['image'].append(HOSTS + i.img6.url)
                if str(i.img7) != "":
                    dict1['image'].append(HOSTS + i.img7.url)
                if str(i.img8) != "":
                    dict1['image'].append(HOSTS + i.img8.url)
                if str(i.img9) != "":
                    dict1['image'].append(HOSTS + i.img9.url)

                context_list.append(dict1)
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