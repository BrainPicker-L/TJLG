from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
import time
import requests
from Tjlg.settings import HOSTS
import os
from Tjlg.settings import MEDIA_ROOT,BASE_DIR
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
from datetime import datetime
# Create your views here.
#安徽大学学号解密
def Sno_Ascll(ascll_word):
    str1 = ""
    for i in range(0, len(ascll_word), 2):
        str1 += chr(int(ascll_word[i] + ascll_word[i + 1]))
    Sno = str1[::-1]
    if Sno[0].isupper() and Sno[2:].isdigit():
        return Sno
    else:
        return ''
#天津理工大学学号解密
def Sno_Ascll_TJLG(ascll_word):
    str1 = ""
    for i in range(0, len(ascll_word), 2):
        str1 += chr(int(ascll_word[i] + ascll_word[i + 1]))
    Sno = str1[::-1]
    if Sno[0:2]=='yk' or Sno[0:2]=='20':
        return Sno
    else:
        return ''

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

        Sno = Sno_Ascll_TJLG(request.POST.get('OnsUha',''))
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
            return HttpResponse(json.dumps({"status": '有数据为空/学号不对'}, ensure_ascii=False))
        # except:
        #     return HttpResponse(json.dumps({"status": "未知错误，联系子哲"}, ensure_ascii=False))
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
                    context['like_users'] = [{'author_id':i.user.id,'author':i.user.Sno,'avatar':HOSTS+i.user.userAvatar.url} for i in UserActionLike.objects.filter(action_id=action.pk)]
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
            #拿到post的数据
            Sno = Sno_Ascll_TJLG(request.POST.get('OnsUha',''))
            userAvatar = request.POST.get('userAvatar', '')
            content = request.POST.get('content','')
            action_id = int(request.POST.get('action_id',1))

            #拿到用户头像的路径
            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            #判断post各值是否为空
            if Sno != '' and content != '' and action_id!='' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()

                # 评论数据入评论数据表
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno, userAvatar=avatar_file_path)
                comment = ArticleComment()
                article_obj = UserAction.objects.get(pk=action_id)
                comment.article = article_obj
                comment.user = user_obj
                comment.content = content
                comment.save()

                noticeCommenters = ArticleComment.objects.filter(article=article_obj)
                snoLst = []
                for noticeCommenter in noticeCommenters:
                    snoLst.append(noticeCommenter.user.Sno)
                snoLst.append(article_obj.author.Sno)
                print(snoLst)
                snoLst = list(set(snoLst))
                snoLst.remove(Sno)
                print(snoLst)
                for targetSno in snoLst:
                    # 评论信息入通知数据表
                    obj = allNotice()
                    obj.movement = "评论"
                    obj.movementer = ahuUser.objects.get(Sno=Sno)
                    obj.action = UserAction.objects.get(id=action_id)
                    obj.noticeer = ahuUser.objects.get(Sno=targetSno)
                    obj.save()

                    #用户未读消息+1
                    objUser = ahuUser.objects.get(Sno=targetSno)
                    objUser.unread_num += 1
                    objUser.save()

                return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({"status": 'post中有值为空/学号不对'}, ensure_ascii=False))




        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲'}, ensure_ascii=False))
    elif request.method == "GET":
        action_id = request.GET.get('action_id','')

        if action_id != '':
            #try:
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
                context['like_users'] = [{'author_id':i.user.id,'author':i.user.Sno,'avatar':HOSTS+i.user.userAvatar.url} for i in
                                              UserCommentLike.objects.filter(comment_id=comment.pk)]

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
            context_dict['like_users'] = [{'author_id':i.user.id,'author':i.user.Sno,'avatar':HOSTS+i.user.userAvatar.url} for i in UserActionLike.objects.filter(action_id=action_obj.pk)]
            time2 = datetime(action_obj.created_time.year, action_obj.created_time.month, action_obj.created_time.day)
            context_dict['commit_count'] = ArticleComment.objects.filter(article_id=action_obj.id).count()
            context_dict['time'] = sort_time((time1 - time2).days, action_obj.created_time)
            if str(action_obj.img) != '':
                context_dict['img'] = HOSTS + action_obj.img.url
            else:
                context_dict['img'] = ''
            context_dict_json = json.dumps(context_dict)
            return HttpResponse(context_dict_json)
        #     except:
        #         context_dict = {}
        #         context_dict_json = json.dumps(context_dict)
        #         return HttpResponse(context_dict_json)
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
            Sno = Sno_Ascll_TJLG(request.POST.get('OnsUha',''))
            userAvatar = request.POST.get('userAvatar', '')
            action_id = int(request.POST.get('action_id', ''))



            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            if Sno != '' and action_id != '' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()

                #将新数据写入动态点赞表
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
                return HttpResponse(json.dumps({"status": 'post中有值为空/学号不对'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲,查看action_id是否不存在'}, ensure_ascii=False))

@csrf_exempt
def change_like_num_comment(request):
    if request.method == "POST":
        try:
            Sno = Sno_Ascll_TJLG(request.POST.get('OnsUha',''))
            userAvatar = request.POST.get('userAvatar', '')
            comment_id = int(request.POST.get('comment_id', ''))

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
                return HttpResponse(json.dumps({"status": 'post中有值为空/学号不对'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲,查看comment_id是否不存在'}, ensure_ascii=False))

@csrf_exempt
def delete_action(request):
    if request.method == "POST":
        try:
            Sno = Sno_Ascll_TJLG(request.POST.get('OnsUha',''))
            author_id = request.POST.get('author_id', '')
            action_id = request.POST.get('action_id', '')
            if Sno and author_id and action_id:
                obj = UserAction.objects.get(author_id=author_id,id=action_id)
                if obj.author.Sno == Sno:
                    obj.delete()
                    return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({"status": '只能删除自己的文章'}, ensure_ascii=False))
            return HttpResponse(json.dumps({"status": 'post中有值为空/学号不对'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲,查看action_id是否不存在'}, ensure_ascii=False))

@csrf_exempt
def delete_comment(request):
    if request.method == "POST":
        try:
            Sno = Sno_Ascll_TJLG(request.POST.get('OnsUha',''))
            comment_id = request.POST.get('comment_id', '')
            action_id = request.POST.get('action_id', '')
            if Sno and comment_id and action_id:
                obj = ArticleComment.objects.get(article_id=action_id,id=comment_id)
                if obj.user.Sno == Sno:
                    obj.delete()
                    return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
                else:
                    return HttpResponse(json.dumps({"status": '只能删除自己的评论'}, ensure_ascii=False))
            return HttpResponse(json.dumps({"status": 'post中有值为空/学号不对'}, ensure_ascii=False))
        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲,查看action_id是否不存在'}, ensure_ascii=False))


#获得个人的通知列表
def notice_lst(request):
    Sno = Sno_Ascll_TJLG(request.GET.get('OnsUha', ''))
    page = request.GET.get('page',1)

    #将未读消息数置零
    print(Sno)
    ahuUesr_obj = ahuUser.objects.get(Sno=Sno)
    ahuUesr_obj.unread_num = 0
    ahuUesr_obj.save()

    #分页显示未读消息列表
    obj_noticeer=ahuUser.objects.get(Sno=Sno)
    notices_all_list = allNotice.objects.filter(noticeer=obj_noticeer).order_by('-create_time')
    paginator = Paginator(notices_all_list, 7)
    if int(page) <= paginator.num_pages:
        if page != '':
            context_list = []
            page_of_notices = paginator.get_page(int(page))
            notices = page_of_notices.object_list
            time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
            for notice in notices:
                context = {}
                context['movement'] = notice.movement
                context['movementer_name'] = notice.movementer.Sno
                context['movementer_avatar'] = HOSTS+notice.movementer.userAvatar.url
                context['excerpt'] = '学号为%s的同学评论了动态'%context['movementer_name']
                context['action_id'] = notice.action.pk
                time2 = datetime(notice.create_time.year, notice.create_time.month, notice.create_time.day)
                print(time2)
                print(time1)
                context['time'] = sort_time((time1 - time2).days, notice.create_time)
                context_list.append(context)
            context_list_json = json.dumps(context_list,ensure_ascii=False)
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


def get_unread_num(request):
    Sno = Sno_Ascll_TJLG(request.GET.get('OnsUha', ''))
    context = {}
    try:
        context['unread_num'] = ahuUser.objects.get(Sno=Sno).unread_num
    except:
        context['unread_num'] = 0
    return HttpResponse(json.dumps(context, ensure_ascii=False))
