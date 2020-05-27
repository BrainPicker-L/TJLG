import requests
import re
import json
from bs4 import BeautifulSoup
from lxml import etree
def login():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    s = requests.session()
    r1 = s.get("http://authserver.tjut.edu.cn/authserver/login",headers=headers)
    r0_1 = s.get("http://authserver.tjut.edu.cn/authserver/captcha.html",headers=headers)
    r0_2 = s.get("http://authserver.tjut.edu.cn/authserver/login",headers=headers)
    data = {
        "lt":re.findall(r'name="lt" value="(.*?)"',r1.text)[0],
        "dllt":re.findall(r'name="dllt" value="(.*?)"',r1.text)[0],
        "execution": re.findall(r'name="execution" value="(.*?)"', r1.text)[0],
        "_eventId": re.findall(r'name="_eventId" value="(.*?)"', r1.text)[0],
        "rmShown": re.findall(r'name="rmShown" value="(.*?)"', r1.text)[0],
        "username":"20170084",
        "password":"123456As"
    }
    print(data)
    print(r1.headers)
    headers = {
        "Origin": "http://authserver.tjut.edu.cn",
        "Referer": "http://authserver.tjut.edu.cn/authserver/login",
        "Host": "authserver.tjut.edu.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    JSESSIONID = requests.utils.dict_from_cookiejar(s.cookies)["JSESSIONID"]
    print(JSESSIONID)
    print(requests.utils.dict_from_cookiejar(s.cookies)["route"])
    r2 = s.post("http://authserver.tjut.edu.cn/authserver/login;jsessionid=%s"%JSESSIONID,data=data,headers=headers)
    #print(r2.text)

    headers = {
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    r3 = s.get("http://ehall.tjut.edu.cn/new/index.html",headers=headers)

    #print(r3.text)


    headers = {
        "Host": "authserver.tjut.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://ehall.tjut.edu.cn/new/index.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    r4 = s.get("http://authserver.tjut.edu.cn/authserver/login?service=http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check",headers=headers)
    ticket = requests.utils.dict_from_cookiejar(s.cookies)["CASTGC"]
    r5_headers = {
        "Host": "ssfw.tjut.edu.cn",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://ehall.tjut.edu.cn/new/index.html",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    }
    r5 = s.get("http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check?ticket=%s"%ticket,headers=r5_headers)
    print(r5.headers)

    r6_headers = {
        "Host": "ssfw.tjut.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://ehall.tjut.edu.cn/new/index.html",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    r6 = requests.get("http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check",headers=r6_headers)

    r7 = s.get("http://ssfw.tjut.edu.cn/ssfw/index.do",headers=r6_headers)
    print(r7.text)
    print(s.cookies)
    # print(requests.utils.dict_from_cookiejar(s.cookies)["iPlanetDirectoryPro"])
    # print(requests.utils.dict_from_cookiejar(s.cookies)["JSESSIONID"])
    # return s

def get_class(s):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
        "Referer":"http://ssfw.tjut.edu.cn/ssfw/index.do"
    }
    class_all_list = []
    xqj_num = [1, 2, 3, 4, 5, 6, 7]
    xqj_han = ["一", "二", "三", "四", "五", "六", "日"]
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
    table = soup.find_all("table", attrs={"class": "ui_table ui_table_striped ui_table_style02"})[0]
    tr_list = table.find_all("tr", attrs={"class": "t_con"})
    for tr in tr_list:
        classInfo_dict = {}
        td_list = tr.find_all("td")
        classInfo_dict["kcmc"] = td_list[2].string
        classInfo_dict["ls"] = str(td_list[7].span).replace("<span>", "").replace("</span>", "").replace("<br/>", ",")
        info_list = str(td_list[5].span).replace("<span>", "").replace("</span>", "").split("节<br/>")  # 分割得到所有上课时间列表
        kcdd_list = str(td_list[6].span).replace("<span>", "").replace("</span>", "").split("<br/>")
        for i in info_list:
            if i == '':
                pass
            else:
                # try:
                if len(info_list) == 1:
                    range1 = (re.findall(r'\d-\d{1,2}节', i)[0])[:-1]

                else:
                    if info_list.index(i) == len(info_list) - 1:
                        range1 = (re.findall(r'\d-\d{1,2}节', i)[0])[:-1]
                    else:
                        range1 = (re.findall(r' \d-\d{1,2}', i)[0]).replace(' ', '')
                classInfo_dict = classInfo_dict.copy()
                range1_list = range1.split("-")
                classInfo_dict['kcdd'] = kcdd_list[info_list.index(i)]
                xqj = (re.findall(r'星期.', i)[0])[-1]
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

                    classInfo_dict["jszs"] = int(re.findall('\d{1,2}', range2_list[1])[0])

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
                    class_all_list = class_all_list + template

                # except:
                #     print(1)

    json_class_all_list = json.dumps(class_all_list, ensure_ascii=False)
    return json_class_all_list
if __name__ == "__main__":
    login()
    #print(get_class(login()))

# iPlanetDirectoryPro=AQIC5wM2LY4SfcwEt%2F8O%2FW99eqVJjJXlaHxdPrkE6FzVvcE%3D%40AAJTSQACMDE%3D%23
# JSESSIONID=fbBT9y8OVg27L4JcWDDOyQKyi1vYHNBaw3U9fG5Uh18W9r5xPNtD!-112387540