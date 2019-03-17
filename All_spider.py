
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
        image.save('/home/TJLG/checkcode1.jpg')
        print("正在拿验证码")
        im = Image.open("/home/TJLG/checkcode1.jpg")
        # imgry = im.convert('L')
        # # 转化到灰度图
        # imgry.save('gray-' + "checkcode1.jpg")
        text = pytesseract.image_to_string(im,lang='fontyp')
        os.remove("/home/TJLG/checkcode1.jpg")
        return text
    def judgeCode(self):    #识别验证码
        # pytesseract.pytesseract.tesseract_cmd = 'd://Tesseract-OCR//tesseract.exe'
        # tessdata_dir_config = '--tessdata-dir "d://Tesseract-OCR//tessdata"'
        while 1:
            im = Image.open("/home/TJLG/checkcode1.jpg")
            # imgry = im.convert('L')
            # # 转化到灰度图
            # imgry.save('gray-' + "checkcode1.jpg")
            text = pytesseract.image_to_string(im,lang='fontyp')
            os.remove("/home/TJLG/checkcode1.jpg")
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
        return json_list_all

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
        return json_class_all_list

    def getTest(self,s,headers):     #拿到考试信息
        data = {
            "xnxqdm": "2018-2019-2"
        }
        url = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"
        r = s.post(url,data=data,headers = headers)
        selector = etree.HTML(r.text)
        all_list = []

        name_list = selector.xpath("/html/body/div[1]/div/fieldset[1]/table//tr/td[3]/text()")
        time_list = selector.xpath("/html/body/div[1]/div/fieldset[1]/table//tr/td[7]/text()")
        position_list = selector.xpath("/html/body/div[1]/div/fieldset[1]/table//tr/td[8]/text()")
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
        # self.getCheckCode(s)
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
                info_json = self.getGrade(s,headers,"2018-2019","1")
            elif choice == "3":
                info_json = self.getTest(s,headers)
            print(info_json)
            return info_json
# a = Test()
# a.main("20170084","liu20056957","1")
