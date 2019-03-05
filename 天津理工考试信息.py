import requests
from PIL import Image
import pytesseract
from lxml import etree
from bs4 import BeautifulSoup
import re
import json
class Test():
    def getCheckCode(self,s):  #获得验证码
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        }
        checkcode = "http://ssfw.tjut.edu.cn/ssfw/jwcaptcha.do?"
        img=s.get(checkcode,stream=True,headers=headers)
        with open('checkcode1.gif','wb') as f:
            f.write(img.content)

    def judgeCode(self):    #识别验证码
        im = Image.open("checkcode1.gif")
        imgry = im.convert('L')
        # 转化到灰度图
        imgry.save('gray-' + "checkcode1.gif")
        text = pytesseract.image_to_string(imgry,lang='fontyp')
        print(text)

        return text

    def getGrade(self,s,headers,term_year,term_num):            #拿到全部成绩

        data = {
            'optype': 'query',
            'isFirst': '1',
            'qXndm_ys':term_year,     #改变学年
            'qXqdm_ys':term_num,             #改变学期
            'qKclbdm_ys':'',
            'qKcxzdm_ys':'',
            'qXdlx_ys':'',
            'qKch_ys':'',
            'qKcm_ys':'',
            'currentSelectTabId': '01',
        }
        r2 = s.post("http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do", data=data, headers=headers)


        list_all = []
        list1 = []
        list2 = []
        xueqi_list = []
        gpa_dict = {}
        soup = BeautifulSoup(r2.text,"lxml")
        b = soup.find("div",attrs={"class":"ui_alert ui_alert_block"})
        gpa_dict['term_year'] = term_year
        gpa_dict['term_num'] = term_num

        gpa_dict['GPA'] = re.findall(r'\d\.\d',str(b))[0]
        a = soup.find_all("div",attrs={"tabid":"01"})[0]
        tr_list = a.find_all('tr', attrs={"class":"t_con"})
        sum_credit = 0
        sum_pa_and_credit = 0
        for tr in tr_list:
            gradeInfo_dict = {}
            td_list = tr.find_all('td')
            #gradeInfo_dict['xueqi'] = td_list[2].string
            gradeInfo_dict['subject'] = td_list[4].string
            gradeInfo_dict['property'] = (td_list[5].string).replace("\xa0","")
            gradeInfo_dict['credit'] = (td_list[8].string)[-4:-1]
            gradeInfo_dict['grade'] = re.findall(r'\d\d',str(td_list[9]))[0]
            if int(gradeInfo_dict['grade'])>=60:
                gradeInfo_dict['pa'] = str(1 + round((int(gradeInfo_dict['grade'])-60)*0.1,2))
            else:
                gradeInfo_dict['pa'] = "0.0"
            list2.append(gradeInfo_dict)
            sum_credit = sum_credit + float(gradeInfo_dict['credit'])
            sum_pa_and_credit = sum_pa_and_credit + float(gradeInfo_dict['credit'])*float(gradeInfo_dict['pa'])

        gpa_dict['term_num_GPA'] = round(sum_pa_and_credit/sum_credit,2)
        gpa_dict['term_year_GPA'] = gpa_dict['term_num_GPA']
        list1.append(gpa_dict)
        list_all.append(list1)
        list_all.append(list2)
        json_list_all = json.dumps(list_all, ensure_ascii=False)
        print(json_list_all)

    def getClass(self,s,headers):
        class_all_list = []
        xqj_num = [1,2,3,4,5,6,7]
        xqj_han = ["一","二","三","四","五","六","七"]
        url = "http://ssfw.tjut.edu.cn/ssfw/xkgl/xkjgcx.do"
        data = {
            'isHistory': 'ss',
            'curPageNo': '2',
            'iDisplayLength': '10',
            'totalSize': '11',
            'qXnxqdm': '2018-2019-2',
            'qKcxzdm':'',
            'qKclbdm':'',
        }
        r = s.post(url,data=data, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find("table", attrs={"class":"ui_table ui_table_striped ui_table_style02"})
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
                    try:
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

                            if range2_list2[1] == "":
                                classInfo_dict["dsz"] = 0
                            else:
                                if (range2_list2[1])[1] == '单':
                                    classInfo_dict["dsz"] = 1
                                elif (range2_list2[1])[1] == '双':
                                    classInfo_dict["dsz"] = 2
                            template = [classInfo_dict][:]
                            class_all_list = class_all_list + template


                    except:
                        print(1)

        json_class_all_list = json.dumps(class_all_list, ensure_ascii=False)
        print(json_class_all_list)

    def getTest(self,s,headers):     #拿到考试信息
        data = {
            "xnxqdm": "2018-2019-1"
        }
        url = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"
        r = s.post(url,data=data,headers = headers)
        selector = etree.HTML(r.text)
        all_list = []

        name_list = selector.xpath("/html/body/div[1]/div/fieldset[1]/table//tr/td[3]/span/text()")
        time_list = selector.xpath("/html/body/div[1]/div/fieldset[1]/table//tr/td[7]/span/text()")
        position_list = selector.xpath("/html/body/div[1]/div/fieldset[1]/table//tr/td[8]/span/text()")
        all_list.append(name_list)
        all_list.append(time_list)
        all_list.append(position_list)
        json_all_list = json.dumps(all_list, ensure_ascii=False)
        print(json_all_list)


    def main(self):
        url = "http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check"
        headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        }
        for i in range(5):
            try:
                s = requests.session()
                self.getCheckCode(s)
                data = {
                    'j_username': '20170084',           #测试用账号密码
                    'j_password': 'liu20056957',
                    'validateCode': self.judgeCode(),
                }
                r = s.post(url,data=data,headers=headers)
                print(r.text)
                self.getClass(s,headers)
                self.getGrade(s,headers,"2018-2019","1")
                self.getTest(s,headers)
                break
            except:
                if i == 4:
                    print("账号密码有误")
                pass

a = Test()
a.main()