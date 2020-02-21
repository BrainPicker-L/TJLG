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

from django.http import JsonResponse
import jieba
import hashlib
# Create your views here.

import requests
import base64


dirty_dict = {
    "无修正": "",
    "被插": "", "裸舞视": "", "春药": "", "秘唇": "", "爱液": "", "乳头": "", "娘西皮": "", "骚水": "", "色情小说": "", "鸡奸": "",
    "迷昏药": "", "狗日的": "", "阴核": "", "拳交": "", "铃声": "", "穴口": "", "妓女": "", "狂操": "", "全家不得好死": "", "人兽": "",
    "裹本": "", "援交": "", "h动漫": "", "干穴": "", "成人卡通": "", "中年美妇": "", "爆乳": "", "寂寞男": "", "狂插": "", "杨思敏": "",
    "阴茎": "", "porn": "", "18禁": "", "麻醉药": "", "阴阜": "", "淫威": "", "我草": "", "屄": "", "草你丫": "", "伦理大": "",
    "肉棍": "", "死全家": "", "淫騷妹": "", "母奸": "", "人渣": "", "抽插": "", "迷昏口": "", "肛门": "", "骚嘴": "", "卧艹": "",
    "菊门": "", "舔阴": "", "少妇": "", "性交图片": "", "要射了": "", "兽交": "", "色情服务": "", "你麻痹": "", "暴乳": "", "淫叫": "",
    "阴唇": "", "狗娘养": "", "马勒": "", "玉乳": "", "成人网站": "", "淫糜": "", "内裤": "", "乖乖粉": "", "性奴集中营": "", "成人游戏": "",
    "性虎": "", "操烂": "", "群交": "", "兽奸": "", "浪妇": "", "口活": "", "狼友": "", "杀b": "", "肉逼": "", "猛男": "",
    "夏川纯": "", "干你娘": "", "a片": "", "迷奸粉": "", "鸡吧": "", "色欲": "", "巨奶": "", "做爱": "", "成人色情": "", "强暴": "",
    "肉茎": "", "色情电影": "", "摇头丸": "", "我就色": "", "性感诱惑": "", "操你全家": "", "大波": "", "风月大陆": "", "密穴": "", "爆你菊": "",
    "美乳": "", "精液": "", "操他妈": "", "高潮": "", "作爱": "", "迷藥": "", "迷情水": "", "拔出来": "", "屁眼": "", "谜奸药": "",
    "贱比": "", "狗杂种": "", "色诱": "", "sb": "", "骚货": "", "插暴": "", "豪乳": "", "欠干": "", "美艳少妇": "", "cao你": "",
    "射颜": "", "幼交": "", "暴淫": "", "漏乳": "", "摸奶": "", "成人文学": "", "骚妇": "", "迷魂藥": "", "一丝不挂": "", "情趣用品": "",
    "色逼": "", "玉穴": "", "快感": "", "擦你妈": "", "淫魔": "", "成人视": "", "阴毛": "", "真他妈": "", "你吗b": "", "肉唇": "",
    "阴间来电": "", "呻吟": "", "美女裸体": "", "美穴": "", "小xue": "", "刹笔": "", "淫虫": "", "咪咪": "", "激情": "", "色b": "",
    "贱b": "", "阴b": "", "incest": "", "学生妹": "", "淫兽": "", "胸推": "", "成人论坛": "", "我日你": "", "大力抽送": "", "阴茎助勃": "",
    "淫亵": "", "玉女心经": "", "sexinsex": "", "写真": "", "淫水": "", "a4u": "", "凌辱": "", "secom": "", "铃木麻": "", "美腿": "",
    "全家死光": "", "轮暴": "", "少修正": "", "肏死": "", "射爽": "", "你他妈": "", "迷奸": "", "下贱": "", "兽欲": "", "汤加丽": "",
    "脱内裤": "", "龟头": "", "轮操": "", "迷奸药": "", "花花公子": "", "火辣": "", "艳情小说": "", "菊花洞": "", "操你妈": "", "内射": "",
    "发情": "", "爆草": "", "日逼": "", "干你妈": "", "裸露": "", "amateur": "", "屌": "", "干死你": "", "淫荡": "", "奶子": "",
    "乳交": "", "叫床": "", "情色": "", "淫兽学": "", "g片": "", "精子": "", "颜射": "", "操死": "", "色情片": "", "淫虐": "",
    "射精": "", "淫荡视频": "", "嫩女": "", "我干": "", "熟妇": "", "粉穴": "", "淫娃": "", "我操": "", "骚比": "", "fuck": "",
    "肉棒": "", "99bb": "", "操黑": "", "阳具": "", "淫浪": "", "裸聊": "", "原味内衣": "", "乳沟": "", "成人图": "", "伦理电影": "",
    "逼奸": "", "骚女": "", "性感妖娆": "", "anal": "", "阉割": "", "阴茎增大": "", "和弦": "", "强jian": "", "阴精": "", "草你吗": "",
    "乱交": "", "成人片": "", "口射": "", "金鳞岂是池中物": "", "别他吗": "", "贱货": "", "色情影片": "", "小逼": "", "换妻俱乐部": "", "色猫": "",
    "色电影": "", "聊性": "", "婊子": "", "品香堂": "", "成人小": "", "诱奸": "", "喷精": "", "自慰": "", "迷昏藥": "", "巨乳": "",
    "插b": "", "吃精": "", "蜜液": "", "一夜欢": "", "淫液": "", "裸聊网": "", "就去日": "", "无耻": "", "色情图片": "", "裙中性运动": "",
    "集体淫": "", "乱奸": "", "色妹妹": "", "迷情粉": "", "招妓": "", "发浪": "", "迷幻藥": "", "仓井空": "", "色情表演": "", "男公关": "",
    "插逼": "", "食精": "", "乳爆": "", "买春": "", "迷魂香": "", "国产av": "", "女优": "", "浑圆": "", "狗操": "", "口爆": "",
    "无码": "", "寂寞女": "", "陰唇": "", "校鸡": "", "插比": "", "g点": "", "成人小说": "", "干你": "", "淫电影": "", "欲仙欲死": "",
    "幼男": "", "xing伴侣": "", "释欲": "", "成人聊": "", "推油": "", "淫河": "", "xiao77": "", "性交": "", "乳房": "", "被干": "",
    "扌由插": "", "盗撮": "", "浪叫": "", "淫书": "", "色小说": "", "性虐": "", "奈美": "", "亚情": "", "捏弄": "", "口淫": "",
    "偷欢": "", "鸡巴": "", "玉蒲团": "", "夜勤病栋": "", "风骚": "", "色视频": "", "淫妻": "", "装b": "", "迷魂药": "", "露b": "",
    "性饥渴": "", "发生关系": "", "sm": "", "粉嫩": "", "操逼": "", "开苞": "", "黑逼": "", "精神药品": "", "性奴": "", "裸体写真": "",
    "卧槽": "", "艹你": "", "成人电": "", "文做": "", "嫩逼": "", "强奸处女": "", "淫媚": "", "煞逼": "", "摸胸": "", "体奸": "",
    "包二奶": "", "丝诱": "", "招鸡": "", "插我": "", "砲友": "", "嫩穴": "", "暴干": "", "沙比": "", "成人dv": "", "伦理片": "",
    "脱光": "", "淫妇": "", "骚逼": "", "熟母": "", "narcotic": "", "混蛋": "", "张筱雨": "", "性爱": "", "肉欲": "", "处男": "",
    "爽死我了": "", "贱人": "", "好嫩": "", "前凸后翘": "", "淫荡美女": "", "淫情": "", "乱伦类": "", "性伙伴": "", "暴奸": "", "男奴": "",
    "裸陪": "", "阴道": "", "一本道": "", "多人轮": "", "插你": "", "日烂": "", "骚穴": "", "陰戶": "", "体位": "", "限量": "",
    "全裸": "", "淫样": "", "一ye情": "", "性福情": "", "调教": "", "妹上门": "", "傻b": "", "性交视频": "", "舞女": "", "adult": "",
    "淫声浪语": "", "性技巧": "", "色情网站": "", "浪女": "", "肥逼": "", "少年阿宾": "", "轮奸": "", "h动画": "", "三级片": "", "肏你": "",
    "色盟": "", "不穿": "", "淫色": "", "黄片": "", "赤裸": "", "干死": "", "口交": "", "sm女王": "", "媚外": "", "按摩": "",
    "成人文": "", "套弄": "", "人妻": "", "淫情女": "", "淫靡": "", "潮吹": "", "兽性": "", "色界": "", "淫魔舞": "", "妈了个逼": "",
    "大sb": "", "一夜情": "", "大乳": "", "操你大爷": "", "偷拍": "", "淫教师": "", "炮友": "", "双臀": "", "抓胸": "", "强奸": "",
    "舔脚": "", "巨屌": "", "欲火": "", "成人电影": "", "几吧": "", "操你祖宗": "", "脚交": "", "白嫩": "", "日你妈": "", "抽一插": "",
    "封面女郎": "", "松岛枫": "", "肉洞": "", "淫兽学园": "", "流淫": "", "阴户": "", "荡妇": "", "乱伦": "", "操我": "", "美幼": "",
    "刺激": "", "肉具": "", "yin荡": "", "爽片": "", "淫穴": "", "迷幻药": "", "肉缝": "", "肛交": "", "性伴侣": "", "小穴": "",
    "淫术炼金士": "", "插进": "", "性欲": "", "性感少": "", "淫荡照片": "", "a4y": "", "自拍": "", "乱伦小": "", "裤袜": "", "淫照": "",
    "应召": "", "gay片": "", "金麟岂是池中物": "", "妈逼": "", "hardcore": "", "兼职": "", "屁股": "", "傻比": "", "妹按摩": "", "美女写真": "",
    "美少妇": "", "后庭": "", "婊子养的": "", "性息": "", "麻痹的": "", "morphine": "", "美逼": "", "熟女": "", "穴图": "", "手淫": "",
    "淫母": "", "裸照": "", "后穴": "", "援助交际": "", "丝袜": "", "淫女": "", "死逼": "", "性服务": "", "揉乳": "", "幼女": "",
    "按摩棒": "", "虎骑": "", "淫贱": "", "浪逼": "", "放尿": "", "欲女": "", "酥痒": "", "骚浪": "", "荡女": "", "被操": "",
    "肉穴": "", "菊穴": "", "狗草": "", "陰道": "", "你妈的": "", "全家死绝": "", "阴蒂": "", "淫乱": "", "吸精": "", "色区": "",
    "相奸": "", "迷情药": "", "插阴": "", "煞笔": "", "白痴": "", "下体": "", "阴部": "", "傻逼": "", "蜜穴": "", "潮喷": "",
    "厕奴": "", "淫肉": "", "奸情": "", "爱女人": "", "tokyohot": "", "伦理毛": "", "操你娘": "", "惹火身材": "", "色色": "", "迷药": "",
    "美女上门": "", "亚砷酸钾": "", "九ping": "", "售健卫": "", "电话监": "", "diacetylmorphine": "", "falungong": "", "爱他死": "",
    "麻古": "", "电狗": "",
    "雄烯二醇": "", "亚硝酰乙氧": "", "普萘洛尔": "", "美沙酮": "", "售单管": "", "自sha": "", "电话拦截器": "", "胰岛素样生长因子": "", "亚砷酸钠": "",
    "推背图": "",
    "法lg": "", "法o功": "", "jiuping": "", "售防身": "", "自fen": "", "甲基安非他明": "", "售步枪": "", "咖啡因": "", "人类灭亡进程表": "",
    "erythropoietin": "",
    "杜冷丁": "", "电警棒": "", "三去车仑": "", "真善忍": "", "麻黄草": "", "明慧网": "", "heroin": "", "售纯度": "", "促红细胞生成素": "",
    "根达亚文明": "",
    "售枪支": "", "统一教": "", "诸世纪": "", "枪决女犯": "", "benzodiazepines": "", "售氯胺": "", "伪火": "", "枪模": "", "tamoxifen": "",
    "氧化铊": "",
    "亚硒酸氢钠": "", "福音会": "", "中国教徒": "", "苯巴比妥": "", "售子弹": "", "电击枪": "", "大法弟子": "", "清海无上师": "", "售假币": "", "大麻": "",
    "售猎枪": "", "海luo因": "", "氯噻嗪": "", "逢八必灾": "", "原子弹方法": "", "逢9必乱": "", "西布曲明": "", "观音法门": "", "氧化汞": "", "轮功": "",
    "地西泮": "", "亚硒酸镁": "", "三唑仑": "", "电鸡": "", "k粉": "", "mdma": "", "fl功": "", "售麻醉": "", "退dang": "", "ketamine": "",
    "法轮": "", "诺查丹玛斯": "", "androst": "", "氧化二丁基锡": "", "明慧周报": "", "售狗子": "", "亚砷（酸）酐": "", "亚硝酸乙酯": "", "甲睾酮": "",
    "suicide": "",
    "集体自杀": "", "售左轮": "", "地塞米松": "", "李洪志": "", "testosterone": "", "电话窃听": "", "逢九必乱": "", "阿芙蓉": "", "原子弹清单": "",
    "售三棱": "",
    "大纪元": "", "9评": "", "枪的制": "", "枪出售": "", "鸦片": "", "退党": "", "枪货到": "", "售热武": "", "dajiyuan": "", "九评": "",
    "法0功": "", "法x功": "", "安非他命": "", "志洪李": "", "发论工": "", "正见网": "", "枪手": "", "diamorphine": "", "氵去车仑": "",
    "按照马雅历法": "",
    "售军用": "", "新型毒品": "", "朱瑟里诺": "", "售弹簧刀": "", "呋塞米": "", "逢8必灾": "", "枪销售": "", "冰毒": "", "尼可刹米": "", "盘古": "",
    "氧氯化磷": "", "电话交友": "", "cannabis": "", "strychnine": "", "法lun": "", "9ping": "", "安眠酮": "", "新唐人": "", "fa轮": "",
    "济世灵文": "",
    "售手枪": "", "苯丙胺": "", "亚硒酸": "", "电话追杀系统": "", "flg": "", "代血浆": "", "氧化亚铊": "", "轮子功": "", "轮法功": "", "地奈德": "",
    "促性腺激素": "", "李宏志": "", "售虎头": "", "枪械制": "", "法一轮一功": "", "tuidang": "", "zi杀": "", "超越红墙": "", "电话定位器": "",
    "海洛因": "",
    "凯他敏": "", "售一元硬": "", "藏字石": "", "亚硒酸二钠": "", "莫达非尼": "", "兴奋剂": "", "原装弹": "", "titor": "", "adrenaline": "",
    "cocain": "",
    "亚硒酸钠": "", "枪子弹": "", "氯胺酮": "", "泼尼松": "", "售火药": "", "吗啡": "", "推bei图": "", "售五四": "", "车仑工力": "", "gong和": "",
    "土g": "", "共x党": "", "gongchandang": "", "共残裆": "", "产党共": "", "共产专制": "", "国wu院": "", "政付": "", "土共": "", "共惨": "",
    "政俯": "", "腐败": "", "供铲党": "", "共铲": "", "老共": "", "gc党": "", "政腐": "", "公产党": "", "裆中央": "", "政f": "",
    "共产党专制": "", "共产党的报应": "", "gong党": "", "zhengfu": "", "中国zf": "", "共贪党": "", "供铲谠": "", "共匪": "", "共残党": "",
    "共残主义": "",
    "共产主义的幽灵": "", "共产王朝": "", "挡中央": "", "恶党": "", "症腐": "", "共产党的末日": "", "正府": "", "g产": "", "communistparty": "",
    "贡挡": "",
    "贪污": "", "供产": "", "共狗": "", "工产党": "", "中gong": "", "g匪": "", "政zhi": "", "gcd": "", "共产党腐败": "", "中珙": "",
    "档中央": "", "拱铲": "", "共c党": "", "供铲裆": "", "北京政权": "", "阿共": "", "仇共": "", "共一产一党": "", "中央zf": "", "中华帝国": "",
    "大陆官方": "", "邪党": "", "狗产蛋": "", "日你": "", "先人板板": "","江泽民":"","膜蛤":"","习近平":"","港独":"","废青":"","胡锦涛":"","郭文贵":""
}

BAIDU_AI = 0

def img_judge(img_path):

    with open(BASE_DIR+img_path.replace(HOSTS,''), 'rb') as f:
        data = {
            "image": base64.b64encode(f.read())
        }
    f.close()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post(
        url="https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined?access_token=24.6c5e1ff107f0e8bcef8c46d3424a0e78.2592000.1485516651.282335-8574074",
        data=data,
        headers=headers,
    )
    print(res.text)
    if json.loads(res.text)["conclusion"] != "合规":
        return os.path.join(HOSTS,"media","community",'img_illegal.png')
    return img_path


def check(content):
    if BAIDU_AI != 0:
        data = {
            "text":content,
        }
        res = requests.post(url="https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=24.6c5e1ff107f0e8bcef8c46d3424a0e78.2592000.1485516651.282335-8574074",data=data)
        if json.loads(res.text)["conclusion"] != "合规":
            return "社区内请文明发言"
    else:
        return content
    # print(content)
    # s = jieba.cut(content,cut_all=True)
    # str = '*'.join(s)
    # jieba_list = str.split('*')
    # print(jieba_list)
    # jieba_list = [i for i in list(set(jieba_list)) if len(i) > 0]
    # print(jieba_list)
    # jieba_list.append(content)
    # for k in jieba_list:
    #     if k in dirty_dict:
    #         content = content.replace(k, '*' * len(k))
    # for k,v in dirty_dict.items():
    #     print(k)
    #     if k in content:
    #         content.replace(k,'*' * len(k))
    #
    # return content


def Sno_Ascll(ascll_word):
    str1 = ""
    return ascll_word
    # for i in range(0, len(ascll_word), 2):
    #     str1 += chr(int(ascll_word[i] + ascll_word[i + 1]))
    # Sno = str1[::-1]
    # if Sno[0].isupper() and Sno[2:].isdigit():
    #     return Sno
    # else:
    #     return ''


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
def upload_img(request):
    choose = request.POST.get("choose","file")
    url = request.POST.get("url","")
    print(choose,url)
    response = []
    if choose == "url":
        if url != '':
            content = requests.get(url=url).content
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(MEDIA_ROOT, "community", os.path.join(md5 + '.jpg'))
            with open(path, 'wb') as f:
                f.write(content)
            if BAIDU_AI == 0:
                img_path = os.path.join(HOSTS, "media", "community", md5 + '.jpg')#img_judge(os.path.join(HOSTS, "media", "community", md5 + '.jpg'))
            else:
                img_path = img_judge(os.path.join(HOSTS, "media", "community", md5 + '.jpg'))
            response.append({'1': "1", 'img_path': img_path})  # 返回前台
            return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:

        files = request.FILES #获取返回来的图片
        for key,value in files.items():
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(MEDIA_ROOT,"community",os.path.join(md5+'.jpg'))
            with open(path, 'wb') as f:
                f.write(content)
            if BAIDU_AI == 0:
                img_path = os.path.join(HOSTS, "media", "community",
                                        md5 + '.jpg')  # img_judge(os.path.join(HOSTS, "media", "community", md5 + '.jpg'))
            else:
                img_path = img_judge(os.path.join(HOSTS, "media", "community", md5 + '.jpg'))
            response.append({'name':key, 'img_path':img_path}) #返回前台
        return HttpResponse(json.dumps(response, ensure_ascii=False))

@csrf_exempt
def useraction(request):
    if request.method == "POST":
        choice = request.POST.get('choice','1')

        Sno = Sno_Ascll(request.POST.get('OnsUha',''))
        wx_name = request.POST.get('wx_name','')
        userAvatar = request.POST.get('userAvatar','')
        excerpt = check(request.POST.get('excerpt',''))
        position = request.POST.get('position', '')
        img = request.POST.get('img','')
        os.chdir(BASE_DIR)
        media_path = './media/'
        avatar_file_path = 'user_avatar/'+Sno+'.gif'



        if userAvatar!='' and excerpt != '' and Sno != '':#"20" in Sno and len(Sno)<12 and userAvatar!='':
            user_obj, created = ahuUser.objects.get_or_create(Sno=Sno)
            if len(Sno)>4:
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                user_obj.userAvatar = avatar_file_path
            user_obj.wx_name = wx_name
            user_obj.save()
            article_obj = UserAction()
            article_obj.author = user_obj
            article_obj.position = position
            print(excerpt)
            article_obj.excerpt = excerpt
            if img!='':
                article_obj.img = img.replace(HOSTS+"/media/",'')
            if choice == "1":
                article_obj.type = ActionType.objects.get(name="个人动态")
            elif choice == "2":
                article_obj.type = ActionType.objects.get(name="失物招领")
            elif choice == "3":
                article_obj.type = ActionType.objects.get(name="有偿悬赏")
            elif choice == "4":
                article_obj.type = ActionType.objects.get(name="二手交易")
            elif choice == "5":
                article_obj.type = ActionType.objects.get(name="校内拼车")
            elif choice == "6":
                article_obj.type = ActionType.objects.get(name="官方")
            elif choice == "7":
                article_obj.type = ActionType.objects.get(name="院系")
            else:
                return  HttpResponse(json.dumps({"status": 'choice不在范围内'}, ensure_ascii=False))
            article_obj.save()
            return HttpResponse(json.dumps({"status": 'success'}, ensure_ascii=False))
        else:
            return HttpResponse(json.dumps({"status": '有数据为空/学号不对'}, ensure_ascii=False))
        # except:
        #     return HttpResponse(json.dumps({"status": "未知错误，联系子哲"}, ensure_ascii=False))
    elif request.method == "GET":
        choice = request.GET.get('choice', "0")
        page = int(request.GET.get('page', 0))
        if choice == "0":
            actions_all_list = UserAction.objects.order_by("-created_time")
        elif choice == "1":
            tmp_name = "个人动态"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")
        elif choice == "2":
            tmp_name = "失物招领"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")
        elif choice == "3":
            tmp_name = "有偿悬赏"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")
        elif choice == "4":
            tmp_name = "二手交易"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")
        elif choice == "5":
            tmp_name = "校内拼车"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")
        elif choice == "6":
            tmp_name = "官方"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")
        elif choice == "7":
            tmp_name = "院系"
            actions_all_list = UserAction.objects.filter(type__name=tmp_name).order_by("-created_time")

        paginator = Paginator(actions_all_list, 7)
        context_list = []
        stickie_actions = stickieAction.objects.all()
        time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)

        # 增加置顶动态列表
        if page == 1 and choice == "0":
            for stickie_action in stickie_actions:
                action = UserAction.objects.get(pk=int(stickie_action.action_id))
                context = {}
                context['author_id'] = action.author.pk
                context['action_id'] = action.pk
                context['author'] = action.author.Sno
                context['wx_name'] = action.author.wx_name

                if str(action.author.userAvatar) != '':
                    context['avatar'] = HOSTS + action.author.userAvatar.url
                else:
                    context['avatar'] = ''
                context['position'] = action.position
                context['excerpt'] = action.excerpt
                context['like_num'] = action.like_num
                if action.type == None:
                    context['type'] = '个人动态'
                else:
                    context['type'] = action.type.name
                context['like_users'] = [
                    {'author_id': i.user.id, 'author': i.user.Sno, 'avatar': HOSTS + i.user.userAvatar.url} for i in
                    UserActionLike.objects.filter(action_id=action.pk)]
                if str(action.img) != '':
                    context['img'] = HOSTS + action.img.url
                else:
                    context['img'] = ''
                context['commit_count'] = ArticleComment.objects.filter(article_id=action.id).count()
                time2 = datetime(action.created_time.year, action.created_time.month, action.created_time.day)
                context['time'] = sort_time((time1 - time2).days, action.created_time)
                context_list.append(context)

        #增加动态列表
        if int(page) <= paginator.num_pages:
            if page != '':

                page_of_actions = paginator.get_page(int(page))
                actions = page_of_actions.object_list

                for action in actions:
                    context = {}
                    context['author_id'] = action.author.pk
                    context['action_id'] = action.pk
                    context['author'] = action.author.Sno
                    context['wx_name'] = action.author.wx_name
                    context['avatar'] = HOSTS + action.author.userAvatar.url
                    context['position'] = action.position
                    context['excerpt'] = action.excerpt
                    context['like_num'] = action.like_num
                    if action.type == None:
                        context['type'] = '个人动态'
                    else:
                        context['type'] = action.type.name
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
            Sno = Sno_Ascll(request.POST.get('OnsUha',''))
            wx_name = request.POST.get('wx_name', '')
            userAvatar = request.POST.get('userAvatar', '')
            content = check(request.POST.get('content',''))
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
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno)
                user_obj.userAvatar = avatar_file_path
                user_obj.wx_name = wx_name
                user_obj.save()
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
            comments = ArticleComment.objects.filter(article_id=action_id).order_by("-like_num")
            context_dict = {}
            context_list = []
            time1 = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
            for comment in comments:
                context = {}
                context['action_id'] = comment.article.pk
                context['commit_id'] = comment.pk
                context["author_id"] = comment.user.pk
                context['author'] = comment.user.Sno
                context['wx_name'] = comment.user.wx_name
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
            context_dict['action_position'] = action_obj.position
            context_dict['action_author_wx_name'] = action_obj.author.wx_name
            context_dict['action_author_avatar'] = HOSTS + action_obj.author.userAvatar.url
            context_dict['action_excerpt'] = action_obj.excerpt
            context_dict['like_num'] = action_obj.like_num
            if action_obj.type == None:
                context_dict['type'] = '个人动态'
            else:
                context_dict['type'] = action_obj.type.name
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
                context['wx_name'] = personal_action.author.wx_name
                context['avatar'] = HOSTS + personal_action.author.userAvatar.url
                context['excerpt'] = personal_action.excerpt
                context['position'] = personal_action.position
                if personal_action.type == None:
                    context_dict['type'] = '个人动态'
                else:
                    context['type'] = personal_action.type.name
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
            context_dict['author_wx_name'] = author_obj.wx_name
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
            Sno = Sno_Ascll(request.POST.get('OnsUha',''))
            userAvatar = request.POST.get('userAvatar', '')
            action_id = int(request.POST.get('action_id', ''))
            wx_name = request.POST.get('wx_name','')



            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            if Sno != '' and action_id != '' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()

                #将新数据写入动态点赞表
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno)
                user_obj.userAvatar=avatar_file_path
                user_obj.wx_name=wx_name
                user_obj.save()
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
            Sno = Sno_Ascll(request.POST.get('OnsUha',''))
            userAvatar = request.POST.get('userAvatar', '')
            comment_id = int(request.POST.get('comment_id', ''))
            wx_name = request.POST.get('wx_name', '')
            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            if Sno != '' and comment_id != '' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                comment_obj = ArticleComment.objects.get(pk=comment_id)
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno)
                user_obj.userAvatar = avatar_file_path
                user_obj.wx_name = wx_name
                user_obj.save()
                like_num, like_num_created = UserCommentLike.objects.get_or_create(user=user_obj, comment=comment_obj,)
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
def get_author_id(request):
    if request.method == "POST":
        try:
            Sno = Sno_Ascll(request.POST.get('OnsUha',''))
            userAvatar = request.POST.get('userAvatar', '')
            wx_name = request.POST.get('wx_name','')
            os.chdir(BASE_DIR)
            media_path = './media/'
            avatar_file_path = 'user_avatar/' + Sno + '.gif'

            if Sno != '' and userAvatar != '':
                with open(media_path + avatar_file_path, 'wb') as f:
                    r = requests.get(url=userAvatar)
                    f.write(r.content)
                f.close()
                user_obj, created = ahuUser.objects.get_or_create(Sno=Sno)
                user_obj.userAvatar = avatar_file_path
                user_obj.wx_name = wx_name
                user_obj.save()
                return HttpResponse(json.dumps({"author_id": str(user_obj.pk)}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({"status": 'post中有值为空/学号不对'}, ensure_ascii=False))

        except:
            return HttpResponse(json.dumps({"status": '未知错误，联系子哲'}, ensure_ascii=False))

@csrf_exempt
def delete_action(request):
    if request.method == "POST":
        try:
            Sno = Sno_Ascll(request.POST.get('OnsUha',''))
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
            Sno = Sno_Ascll(request.POST.get('OnsUha',''))
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
    Sno = Sno_Ascll(request.GET.get('OnsUha', ''))
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
                context['movementer_name'] = notice.movementer.wx_name
                context['movementer_avatar'] = HOSTS+notice.movementer.userAvatar.url
                context['excerpt'] = '【%s】同学评论了动态'%context['movementer_name']
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
    Sno = Sno_Ascll(request.GET.get('OnsUha', ''))
    context = {}
    try:
        context['unread_num'] = ahuUser.objects.get(Sno=Sno).unread_num
    except:
        context['unread_num'] = 0
    return HttpResponse(json.dumps(context, ensure_ascii=False))
