
import requests
from PIL import Image
import pytesseract
from lxml import etree
from bs4 import BeautifulSoup
import re
import json
import os
import time
from io import BytesIO
from gradeList.models import *
class Library():
    def getBookinfo(self,keyword,page):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        }
        url = "http://libm.tjut.edu.cn/fwd6.php?keyword="+keyword+"&nextindex="+str((int(page)-1)*20+1)+"&searchtype=1"         #一页有20条数据
        r = requests.get(url,headers=headers)
        info_json = json.loads(r.text)
        all_pageNum = info_json['totals']       #结果总数
        books_info_json = json.dumps(info_json['items'], ensure_ascii=False)
        return books_info_json   #books_info_json是搜到的书结果json

class Test():
    # def getCheckCode(self,s):  #获得验证码
    #     headers = {
    #         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
    #     }
    #     checkcode = "http://ssfw.tjut.edu.cn/ssfw/jwcaptcha.do?"
    #     img=s.get(checkcode,stream=True,headers=headers)
    #     with open('checkcode1.gif','wb') as f:
    #         f.write(img.content)
    def getCheckCode(self,s):
        headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        }
        img_src = "http://ssfw.tjut.edu.cn/ssfw/jwcaptcha.do?"
        response = s.get(img_src,headers=headers)
        image = Image.open(BytesIO(response.content))
        # imgry = im.convert('L')
        # # 转化到灰度图
        # imgry.save('gray-' + "checkcode1.jpg")
        text = pytesseract.image_to_string(image,lang='fontyp')
        return text


    def getGrade(self,s,headers,term_year,term_num_list,user):            #拿到全部成绩
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
            r2 = s.post("http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do", data=data, headers=headers)
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

            obj, created = student_Id.objects.get_or_create(xuehao=user)
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
                    obj, created = gradeInfo.objects.get_or_create(grade_id=grade_id,unique_key=user+"_"+grade_id,subject=gradeInfo_dict['subject'],property=gradeInfo_dict['property'],grade=gradeInfo_dict['grade'])
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

    def getAllGrade(self,s,headers,user):            #拿到全部成绩

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
        r2 = s.post("http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do", data=data, headers=headers)



        soup = BeautifulSoup(r2.text, "lxml")
        b = soup.find("div", attrs={"class": "ui_alert ui_alert_block"})


        a = soup.find_all("div", attrs={"tabid": "01"})[0]
        tr_list = a.find_all('tr', attrs={"class": "t_con"})

        obj, created = student_Id.objects.get_or_create(xuehao=user)
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
            print(grade_id)
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
            print(gradeInfo_dict['subject'],td_list[4],td_list[4].string)
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
                    gradeInfo_dict['grade'] = re.findall(r'\d{1,3}', str(td_list[9]))[0]
                else:
                    gradeInfo_dict['grade'] = gradeInfo_dict['grade'][0]
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
        print(xueian_dict)
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

    def getClass(self,s,headers):
        class_all_list = []
        xqj_num = [1,2,3,4,5,6,7]
        xqj_han = ["一","二","三","四","五","六","日"]
        url = "http://ssfw.tjut.edu.cn/ssfw/xkgl/xkjgcx.do"
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
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
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
                        range1 = (re.findall(r'\d-\d{1,2}节',i)[0])[:-1]

                    else:
                        if info_list.index(i) == len(info_list)-1:
                            range1 = (re.findall(r'\d-\d{1,2}节', i)[0])[:-1]
                        else:
                            range1 = (re.findall(r' \d-\d{1,2}', i)[0]).replace(' ','')
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
                        obj,created = ClassInfo.objects.get_or_create(kcmc=classInfo_dict['kcmc'],ls=classInfo_dict['ls'],kcdd=classInfo_dict['kcdd'],xqj=classInfo_dict['xqj'],skjc=classInfo_dict['skjc'],skcd=classInfo_dict['skcd'],qszs=classInfo_dict['qszs'],jszs=classInfo_dict['jszs'],dsz=classInfo_dict['dsz'],extra=extra)

                        class_all_list = class_all_list + template


                    # except:
                    #     print(1)

        json_class_all_list = json.dumps(class_all_list, ensure_ascii=False)
        return json_class_all_list

    def getTest(self,s,headers):     #拿到考试信息
        data = {
            "xnxqdm": "2019-2020-1"
        }
        url = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"
        r = s.post(url,data=data,headers = headers)
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




    def main(self,user,password,choice):

        url = "http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check"
        headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        }

        s = requests.session()

        # try:
        while 1:

            data = {
                'j_username': user,           #测试用账号密码
                'j_password': password,
                'validateCode': self.getCheckCode(s),
            }
            print(data)
            if data["validateCode"] == '':
                continue
            r = s.post(url,data=data,headers=headers)
            return_info = r.text.split("\":")[0].replace("{", "").replace("\"", "")
            print(return_info)
            if return_info == "success":
                break
            elif return_info == "userNameOrPasswordError":
                break
            elif return_info == "validateCodeError":
                continue



        if return_info == "userNameOrPasswordError":
            info_json = json.dumps({"error":-2}, ensure_ascii=False)
            return info_json
        elif return_info == "success":
            if choice == "1":
                info_json = self.getClass(s,headers)
            elif choice == "2":
                info_json = self.getGrade(s,headers,"2018-2019",["1","2"],user)
            elif choice == "3":
                info_json = self.getTest(s,headers)
            elif choice == "4":
                info_json = self.getAllGrade(s,headers,user)
            print(info_json)
            return info_json
        # except:
        #     info_json = json.dumps({"error":-4}, ensure_ascii=False)
        #     return info_json
