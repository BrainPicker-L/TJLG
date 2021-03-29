import re
import json
import copy
import requests
from requests.adapters import HTTPAdapter
from lxml import etree
from bs4 import BeautifulSoup
import random
import traceback


def pre_log_tj(s,stu_num, password,headers):
    """
    模拟登陆教务系统，异地检测
    :return:
    """
    # 第一次请求
    pre_login_url = "http://authserver.tjut.edu.cn/authserver/login?service=http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check"
    headers_pre = copy.deepcopy(headers)
    # headers_pre['User-Agent'] = random.choice(user_agent)
    r = s.get(pre_login_url, headers=headers_pre)
    cookie = requests.utils.dict_from_cookiejar(r.cookies)

    # 再次请求，拿到跳转地址
    pre_login_url_again = "http://authserver.tjut.edu.cn/authserver/login;jsessionid={}?service=http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check"
    # print(cookie)
    # 构造 headers
    reg_lt_value = r'<input type="hidden" name="lt" value="(.*?cas)"'
    print(r.text)
    lt_value = re.findall(reg_lt_value, r.text)[0]
    headers_pre_again = copy.deepcopy(headers_pre)
    # headers_pre_again['Origin'] = 'http://authserver.tjut.edu.cn'
    headers_pre_again['Referer'] = 'http://authserver.tjut.edu.cn/authserver/login?service=http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check'
    headers_pre_again['Cookie'] = str('route='+cookie['route']+';'+'JSESSIONID='+cookie['JSESSIONID'])
    headers_pre_again['Content-Type'] = 'application/x-www-form-urlencoded'
    headers_pre_again['Content-Length'] = '170'
    # 构造数据
    data = {
        'username': stu_num,
        'password':  password,
        'lt': lt_value,
        'dllt': 'userNamePasswordLogin',
        'execution': 'e1s1',
        '_eventId': 'submit',
        'rmShown': 1,
    }
    r_again = s.post(pre_login_url_again.format(cookie['JSESSIONID']), headers=headers_pre_again, data=data, allow_redirects=False)
    # 利用正则取的 跳转 url 和 iPlanetDirectoryPro
    # reg_ipd = r'iPlanetDirectoryPro=(.*?);'
    reg_url = r"<p>It's now at <a href=\"(.*?-cas)\""
    reg_real_url = re.findall(reg_url, r_again.text)[0]

    cookie_again = requests.utils.dict_from_cookiejar(r_again.cookies)
    ipd = cookie_again['iPlanetDirectoryPro']
    # set_cookie = r_again.headers['Set-Cookie']
    # ipd = re.findall(reg_ipd, set_cookie)[0]
    # print(reg_real_url)
    # print(set_cookie)
    # print(ipd)
    return reg_real_url, headers_pre_again['User-Agent'], ipd


def log_tj(s,stu_num, password,headers):
    """
    跳转登陆，需再次进行检测
    :return:
    """
    log_headers = {
        "Accept-Language": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Host": "ssfw.tjut.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Referer": 'http://authserver.tjut.edu.cn/authserver/login?service=http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check',
    }
    url, ua, ipd = pre_log_tj(s,stu_num, password,headers)
    print(url)
    r = s.get(url, headers=log_headers, allow_redirects=False)
    cookie = requests.utils.dict_from_cookiejar(r.cookies)
    # print(cookie)
    # print(r.headers['Set-Cookie'])
    # 获取 新 JSESSIONID
    jid = cookie['JSESSIONID']
    # print(jid)
    # print(jid)
    # 进行异地检测
    url_yidi = 'http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check'
    log_headers['Cookie'] = 'iPlanetDirectoryPro='+ipd+';'+'JSESSIONID=' + jid
    yidi_r = s.get(url_yidi, headers=log_headers)
    # print(yidi_r.text)
    #  访问选课管理

    xk_headers = copy.deepcopy(log_headers)
    xk_headers['DNT'] = '1'
    xk_headers['Upgrade-Insecure-Requests'] = '1'
    xk_headers['Referer'] = 'http://ssfw.tjut.edu.cn/ssfw/index.do'
    xk_headers['User-Agent'] = ua
    xk_headers['Cookie'] = 'iPlanetDirectoryPro='+ipd+';'+'JSESSIONID=' + jid

    return xk_headers

def getClass(s,xk_headers):
    class_all_list = []
    xqj_num = [1,2,3,4,5,6,7]
    xqj_han = ["一","二","三","四","五","六","日"]
    url = r'http://ssfw.tjut.edu.cn/ssfw/xkgl/xkjgcx.do'
    # data = {
    #     'isHistory': 'ss',
    #     'curPageNo': '1',
    #     'iDisplayLength': '20',
    #     'totalSize': '20',
    #     'qXnxqdm': '2019-2020-2',
    #     'qKcxzdm':'',
    #     'qKclbdm':'',
    # }
    # r = s.post(url, headers=headers,data=data)


    r_text = s.get(url, headers=xk_headers).text
    soup = BeautifulSoup(r_text, "lxml")
    table = soup.find_all("table", attrs={"class":"ui_table ui_table_striped ui_table_style02"})[0]
    tr_list = table.find_all("tr", attrs={"class":"t_con"})
    for tr in tr_list:
        classInfo_dict = {}
        td_list = tr.find_all("td")
        classInfo_dict["kcmc"] = td_list[2].string
        classInfo_dict["ls"] = str(td_list[7].span).replace("<span>","").replace("</span>","").replace("<br/>",",")
        info_list = str(td_list[5].span).replace("<span>","").replace("</span>","").split("节<br/>")     #分割得到所有上课时间列表
        kcdd_list = str(td_list[6].span).replace("<span>","").replace("</span>","").split("<br/>")
        for i in info_list:
            if i == '':
                pass
            else:
                #try:
                if len(info_list)==1:
                    range1 = (re.findall(r'\d{1,2}-\d{1,2}节',i)[0])[:-1]

                else:
                    if info_list.index(i) == len(info_list)-1:
                        range1 = (re.findall(r'\d{1,2}-\d{1,2}节', i)[0])[:-1]
                    else:
                        range1 = (re.findall(r' \d{1,2}-\d{1,2}', i)[0]).replace(' ','')
                classInfo_dict = classInfo_dict.copy()
                range1_list = range1.split("-")
                classInfo_dict['kcdd'] = kcdd_list[info_list.index(i)]
                xqj = (re.findall(r'星期.',i)[0])[-1]
                classInfo_dict["xqj"] = xqj_num[xqj_han.index(xqj)]
                # classInfo_dict["xqj"] = (re.findall(r'星期.', i)[0])[-1]
                classInfo_dict["skjc"] = int(range1_list[0])
                classInfo_dict["skcd"] = int(int(range1_list[1]) - int(range1_list[0]) + 1)
                range2 = re.finditer(r'\d{1,2}-\d{1,2}周(\(.\))?', i)
                for j in range2:
                    classInfo_dict = classInfo_dict.copy()
                    range2_list = j.group().split("-")
                    classInfo_dict["qszs"] = int(range2_list[0])
                    range2_list2 = range2_list[1].split("周")

                    classInfo_dict["jszs"] = int(re.findall('\d{1,2}',range2_list[1])[0])

                    extra = "课程：%s\n老师：%s\n上课地点：%s\n上课时间：星期%s 第%s节-第%s节 %s-%s周" % (
                    classInfo_dict['kcmc'], classInfo_dict["ls"], classInfo_dict['kcdd'], xqj,
                    classInfo_dict["skjc"], classInfo_dict["skjc"] + classInfo_dict["skjc"],
                    classInfo_dict["qszs"], classInfo_dict["jszs"])

                    if range2_list2[1] == "":
                        classInfo_dict["dsz"] = 0
                    else:
                        if (range2_list2[1])[1] == '单':
                            classInfo_dict["dsz"] = 1
                            extra += "(单周)"
                        elif (range2_list2[1])[1] == '双':
                            classInfo_dict["dsz"] = 2
                            extra += "(双周)"
                    template = [classInfo_dict][:]
                    #obj,created = ClassInfo.objects.get_or_create(kcmc=classInfo_dict['kcmc'],ls=classInfo_dict['ls'],kcdd=classInfo_dict['kcdd'],xqj=classInfo_dict['xqj'],skjc=classInfo_dict['skjc'],skcd=classInfo_dict['skcd'],qszs=classInfo_dict['qszs'],jszs=classInfo_dict['jszs'],dsz=classInfo_dict['dsz'],extra=extra)

                    class_all_list = class_all_list + template


                # except:
                #     print(1)

    json_class_all_list = json.dumps(class_all_list, ensure_ascii=False)
    return json_class_all_list

def getGrade(s,term_year,term_num_list,xk_headers):            #拿到全部成绩
    list2 = []
    sum_credit = 0
    sum_pa_and_credit = 0
    for term_num in term_num_list:
        data = {
            'optype': 'query',
            'isFirst': '1',
            'qXndm_ys': term_year,  # 改变学年
            'qXqdm_ys': term_num,  # 改变学期
            'qKclbdm_ys': '',
            'qKcxzdm_ys': '',
            'qXdlx_ys': '',
            'qKch_ys': '',
            'qKcm_ys': '',
            'currentSelectTabId': '01',
        }
        r2 = s.post("http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do", data=data, headers=xk_headers)
        list_all = []
        list1 = []

        xueqi_list = []
        gpa_dict = {}
        soup = BeautifulSoup(r2.text, "lxml")
        b = soup.find("div", attrs={"class": "ui_alert ui_alert_block"})
        gpa_dict['term_year'] = term_year
        gpa_dict['term_num'] = term_num

        gpa_dict['GPA'] = re.findall(r'\d\.\d|\d', str(b))[0]
        a = soup.find_all("div", attrs={"tabid": "01"})[0]
        tr_list = a.find_all('tr', attrs={"class": "t_con"})


        for tr in tr_list:
            try:
                gradeInfo_dict = {}
                td_list = tr.find_all('td')
                # gradeInfo_dict['xueqi'] = td_list[2].string
                grade_id = td_list[3].string
                gradeInfo_dict['subject'] = td_list[4].string
                gradeInfo_dict['property'] = (td_list[5].string).replace("\xa0", "")
                gradeInfo_dict['credit'] = (td_list[8].string)[-4:-1]
                gradeInfo_dict['grade'] = re.findall(r'\d{1,3}', str(td_list[9]))[0]
                if int(gradeInfo_dict['grade']) >= 60:
                   # gradeInfo_dict['pa'] = str(1 + round((int(gradeInfo_dict['grade']) - 60) * 0.1, 2))
                    gradeInfo_dict['pa'] = str(((int(gradeInfo_dict['grade']))-60)//5*0.5+1)
                else:
                    gradeInfo_dict['pa'] = "0.0"
                list2.append(gradeInfo_dict)
                sum_credit = sum_credit + float(gradeInfo_dict['credit'])
                sum_pa_and_credit = sum_pa_and_credit + float(gradeInfo_dict['credit']) * float(gradeInfo_dict['pa'])
                #obj, created = gradeInfo.objects.get_or_create(grade_id=grade_id,unique_key=user+"_"+grade_id,subject=gradeInfo_dict['subject'],property=gradeInfo_dict['property'],grade=gradeInfo_dict['grade'])
                # if created == True:
                #     Grade = gradeInfo()
                #     Grade.grade_id = grade_id
                #     Grade.subject = gradeInfo_dict['subject']
                #     Grade.property = gradeInfo_dict['property']
                #     Grade.grade = gradeInfo_dict['grade']
                #     Grade.save()

            except:
                pass
    gpa_dict['term_num_GPA'] = round(sum_pa_and_credit / sum_credit, 2)
    gpa_dict['term_year_GPA'] = gpa_dict['term_num_GPA']
    list1.append(gpa_dict)
    list_all.append(list1)
    list_all.append(list2)
    json_list_all = json.dumps(list_all, ensure_ascii=False)
    return json_list_all

def getAllGrade(s,xk_headers):            #拿到全部成绩

    #try:
    data = {
        'optype': 'query',
        'isFirst': '1',
        'qXndm_ys': '',  # 改变学年
        'qXqdm_ys': '',  # 改变学期
        'qKclbdm_ys': '',
        'qKcxzdm_ys': '',
        'qXdlx_ys': '',
        'qKch_ys': '',
        'qKcm_ys': '',
        'currentSelectTabId': '01',
    }

    r2 = s.post("http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do", data=data, headers=xk_headers)
    #print(r2.text)



    soup = BeautifulSoup(r2.text, "lxml")
    b = soup.find("div", attrs={"class": "ui_alert ui_alert_block"})


    a = soup.find_all("div", attrs={"tabid": "01"})[0]
    tr_list = a.find_all('tr', attrs={"class": "t_con"})

    xnxq_lst = []

    xq_dict = {"一":'1',"二":'2','三':'3'}
    all_list = []
    zongjidian = re.findall(r'\d\.\d|\d', str(b))[0]
    dict1 = {"xn":'','xq':'','zongjidian':zongjidian,'xq_jidian':0,'xn_jidian':0,'all_credit':0,'all_credit_jiaquan':0,'grade_list':[]}

    for tr in tr_list:
        gradeInfo_dict = {}
        td_list = tr.find_all('td')
        # gradeInfo_dict['xueqi'] = td_list[2].string
        grade_id = td_list[3].string
        #print(grade_id)
        xn = re.findall(r'(.*)学年', td_list[2].string)[0]
        xq = xq_dict[re.findall(r'学年第(.*?)学期', td_list[2].string)[0]]
        if xn +"_"+xq not in xnxq_lst:
            xnxq_lst.append(xn +"_"+xq)
            if dict1["all_credit"]:
                dict1["xq_jidian"] = round(dict1['all_credit_jiaquan']/dict1["all_credit"],2)
            all_list.append(dict1)
            dict1 = {"xn": '', 'xq': '', 'zongjidian': zongjidian, 'xq_jidian': 0, 'xn_jidian': 0, 'all_credit': 0,
                     'all_credit_jiaquan': 0, 'grade_list': []}
            dict1["xn"] = xn
            dict1["xq"] = xq

        gradeInfo_dict['subject'] = str(td_list[4].string)
        if gradeInfo_dict['subject'] == 'None':
            gradeInfo_dict['subject'] = re.findall(r'<td align="center" valign="middle">(.*?)</s></td>',str(td_list[4]))[0].replace('<br/><s style="color: red">','\\')
        #print(gradeInfo_dict['subject'],td_list[4],td_list[4].string)
        gradeInfo_dict['property'] = (td_list[5].string).replace("\xa0", "")
        gradeInfo_dict['credit'] = td_list[8].string
        if gradeInfo_dict['credit'] != None:
            gradeInfo_dict['credit'] = float(gradeInfo_dict['credit'][-4:-1])
            gradeInfo_dict['grade'] = re.findall(r'\d{1,3}', str(td_list[9]))[0]
            if int(gradeInfo_dict['grade']) >= 60:
               # gradeInfo_dict['pa'] = str(1 + round((int(gradeInfo_dict['grade']) - 60) * 0.1, 2))
                gradeInfo_dict['pa'] = ((int(gradeInfo_dict['grade']))-60)//5*0.5+1
            else:
                gradeInfo_dict['pa'] = 0
            dict1["all_credit"] += gradeInfo_dict["credit"]
            dict1["all_credit_jiaquan"] += gradeInfo_dict["pa"] * gradeInfo_dict["credit"]
        else:
            gradeInfo_dict['grade'] = re.findall(r'<strong>(.*?)</strong>',str(td_list[9]))
            if gradeInfo_dict['grade'] == []:
                try:
                    gradeInfo_dict['grade'] = re.findall(r'\d{1,3}', str(td_list[9]))[0]
                except:
                    gradeInfo_dict['grade'] = re.findall(r'[\u4e00-\u9fa5]+', str(td_list[9]))
                    if gradeInfo_dict != []:
                        gradeInfo_dict['grade'] = gradeInfo_dict['grade'][0]
                    else:
                        gradeInfo_dict['grade'] = ""
            else:
                gradeInfo_dict['grade'] = gradeInfo_dict['grade'][0]
        #print(str(td_list[9]))
        dict1["grade_list"].append(gradeInfo_dict)
        # obj, created = gradeInfo.objects.get_or_create(grade_id=grade_id, unique_key=user + "_" + grade_id,
        #                                                    subject=gradeInfo_dict['subject'],
        #                                                    property=gradeInfo_dict['property'],
        #                                                    grade=gradeInfo_dict['grade'])

    xnxq_lst.append(xn + "_" + xq)
    if dict1["all_credit"]:
        dict1["xq_jidian"] = round(dict1['all_credit_jiaquan'] / dict1["all_credit"], 2)
    all_list.append(dict1)

    all_list = all_list[1:]

    pre = ''
    xuefen_xuenian = 0
    xuefen_xuenian_all = 0
    xueian_dict = {}
    for j in all_list:
        if j['xn'] == pre or pre == '':
            xuefen_xuenian += j["all_credit"]
            xuefen_xuenian_all += j["all_credit_jiaquan"]
        elif j['xn'] != pre and pre != '':
            xueian_dict[pre] = round(xuefen_xuenian_all / xuefen_xuenian, 2)
            xuefen_xuenian = 0
            xuefen_xuenian_all = 0
            xuefen_xuenian += j["all_credit"]
            xuefen_xuenian_all += j["all_credit_jiaquan"]
        pre = j['xn']
    xueian_dict[pre] = round(xuefen_xuenian_all / xuefen_xuenian, 2)
    #print(xueian_dict)
    for i in all_list:
        for k, v in xueian_dict.items():
            if i['xn'] == k:
                i["xn_jidian"] = v
                break



    json_list_all = json.dumps(all_list, ensure_ascii=False)
    return json_list_all

    # except:
    #     json_list_all = json.dumps({"error": "暂未评教，请登录信息门户评教后可查看"}, ensure_ascii=False)
    #     return json_list_all

def getTest(s,xk_headers):     #拿到考试信息
    data = {
        "xnxqdm": "2020-2021-1"
    }
    url = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"
    r = s.post(url,data=data,headers = xk_headers)
    selector = etree.HTML(r.text)
    all_list = []

    name_list = selector.xpath('//div[@class="div_body"]/fieldset[1]/table[@class="ui_table ui_table_hover ui_table_striped ui_table_style02"]//tr[@class="t_con"]/td[3]//text()')
    time_list = selector.xpath('//div[@class="div_body"]/fieldset[1]/table[@class="ui_table ui_table_hover ui_table_striped ui_table_style02"]//tr[@class="t_con"]/td[7]//text()')
    position_list = selector.xpath('//div[@class="div_body"]/fieldset[1]/table[@class="ui_table ui_table_hover ui_table_striped ui_table_style02"]//tr[@class="t_con"]/td[8]//text()')
    for i in range(len(name_list)):
        dict1 = {}
        dict1['KCMC'] = name_list[i]
        dict1['KSSJ'] = time_list[i]
        dict1['JSMC'] = position_list[i]
        all_list.append(dict1)
    json_all_list = json.dumps(all_list, ensure_ascii=False)
    return json_all_list
def main(stu_num,password,choice):
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            # iPhone 6：
            "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
        ]
        headers = {
            "Accept-Language": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Host": "authserver.tjut.edu.cn",
            "User-Agent":  random.choice(user_agent),#"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        }

        choice=str(choice)
        xk_headers = log_tj(s,stu_num, password,headers)

        if choice == "1":
            info_json = getClass(s,xk_headers)
        elif choice == "2":
            info_json = getGrade(s,"2018-2019",["1","2"],xk_headers)
        elif choice == "3":
            info_json = getTest(s,xk_headers)
        elif choice == "4":
            info_json = getAllGrade(s,xk_headers)
        else:
            info_json = "choice error"
        return info_json
    except:
        #print(traceback.format_exc())
        return  json.dumps({"error": "用户名/密码错误"}, ensure_ascii=False)


if __name__ == "__main__":
    stu_num = '20200631'  # input("请输入学号：")
    password = 'zky-200101040011'  # input("请输入密码：")
    print(main(stu_num,password,1))
