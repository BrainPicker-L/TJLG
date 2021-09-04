# -*- coding: utf-8 -*-

import execjs
import json
import os
import re
import requests

from lxml import etree


class TJLG_University:

    def __init__(self, username, pwd):
        self.username = username
        self.pwd = pwd
        self.login_url = "http://authserver.tjut.edu.cn/authserver/login"
        self.session = requests.session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        self.session.headers.update(self.headers)
        self.xqj_dict = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "日"}
        self.dsz_dict = {"单": 1, "双": 2}

    @staticmethod
    def _load_js():
        with open("script/sdk.js", mode="r", encoding="utf-8") as f:
            return execjs.compile(f.read())

    @staticmethod
    def _save_to_json(name, data_list):
        if not os.path.exists("json"):
            os.mkdir("json")
        with open(f"./json/{name}.json", mode="w", encoding="utf-8") as f:
            f.write(json.dumps(data_list, ensure_ascii=False))

    def get_salt(self):
        response = self.session.get(self.login_url)
        xpathor = etree.HTML(response.text)
        lt = xpathor.xpath(".//input[@name='lt']/@value")[0]
        salt = xpathor.xpath(".//input[@id='pwdDefaultEncryptSalt']/@value")[0]
        execution = xpathor.xpath(".//input[@name='execution']/@value")[0]
        return lt, salt, execution

    def login(self):
        etx = self._load_js()
        lt, salt, execution = self.get_salt()
        enc_pwd = etx.call("enc_pwd", self.pwd, salt)
        data = {
            "username": self.username,
            "password": enc_pwd,
            "lt": lt,
            "dllt": "userNamePasswordLogin",
            "execution": execution,
            "_eventId": "submit",
            "rmShown": "1",
        }
        self.session.post(self.login_url, data=data)
        self.session.get("http://ssfw.tjut.edu.cn/ssfw/cas_index.jsp")

    def _by_info_get_dict_data(self, data_list, j, info):
        kcmc = info[0].split(" ")[0].split("[")[0]
        ls = info[1]
        kcdd = info[2].strip()
        xqj = j + 1
        sk = re.findall(r"\d+", info[0].split(" ")[2])
        skjc = sk[0]
        skcd = len(sk)
        zs_info = info[0].split(" ")[1]
        ds_info = re.findall(r"\((.*?)\)", zs_info, re.S)
        if not ds_info:
            dsz = 0
        else:
            dsz = self.dsz_dict[ds_info[0]]
        zs_info_list = zs_info.split(",")
        for zs_info in zs_info_list:
            zs = re.findall(r"\d+", zs_info)
            qszs = zs[0]
            jszs = zs[1]
            extra = f"课程：{kcmc}\n老师：{ls}\n上课地点：{kcdd}\n上课时间：星期{self.xqj_dict[xqj]} {info[0].split(' ')[2][1:-1]} {zs_info}"
            dict_data = {
                "kcmc": kcmc,
                "ls": ls,
                "kcdd": kcdd,
                "xqj": xqj,
                "skjc": int(skjc),
                "skcd": int(skcd),
                "qszs": int(qszs),
                "jszs": int(jszs),
                "dsz": dsz,
                "extra": extra,
            }
            data_list.append(dict_data)

    def parse_course(self, param_dict):
        url = f"http://ssfw.tjut.edu.cn/ssfw/pkgl/kcbxx/4/{param_dict['xn']}-{param_dict['xq']}.do"
        response = self.session.get(url)
        xpathor = etree.HTML(response.text)
        tr_list = xpathor.xpath(".//table[@id='1']/tr")[1:-1]

        data_list = []
        for i, tr in enumerate(tr_list):
            for j, td in enumerate(tr.xpath("./td")[2:]):
                info = [text.replace("\xa0", "").strip("\n") for text in td.xpath(".//text()")]
                if info == [""]:
                    continue
                else:
                    info = list(filter(None, info))
                    if len(info) == 6:
                        infos = [[info[0], info[1], info[2]], [info[3], info[4], info[5]]]
                        for info in infos:
                            self._by_info_get_dict_data(data_list, j, info)
                    elif len(info) == 3:
                        self._by_info_get_dict_data(data_list, j, info)
        self._save_to_json("course", data_list)

    def parse_grade(self, param_dict):
        api = "http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do"
        data = {
            "optype": "query",
            "isFirst": "1",
            "qXndm_ys": param_dict["xn"],
            "qXqdm_ys": param_dict["xq"],
            "qKclbdm_ys": "",
            "qKcxzdm_ys": "",
            "qXdlx_ys": "",
            "qKch_ys": "",
            "qKcm_ys": "",
            "currentSelectTabId": "01"
        }
        response = self.session.post(api, data=data)
        xpathor = etree.HTML(response.text)
        tr_list = xpathor.xpath(".//tr[@class='t_con']")

        data_list = []
        for index, tr in enumerate(tr_list):
            stuId = self.username
            className = tr.xpath("./td[5]/text()")[0].replace("\xa0", "")
            try:
                grade = int(list(filter(None, [_.replace("\r", "").replace("\t", "").strip() for _ in tr.xpath("./td[10]//text()")]))[0])
            except ValueError:
                grade = list(filter(None, [_.replace("\r", "").replace("\t", "").strip() for _ in tr.xpath("./td[10]//text()")]))[0]
            classId = tr.xpath("./td[4]/text()")[0].replace("\xa0", "")
            category = tr.xpath("./td[6]/text()")[0].replace("\xa0", "")
            try:
                score = float(tr.xpath('./td[9]/text()')[0].replace("\xa0", "").strip())
            except IndexError:
                score = ""
            classNature = tr.xpath("./td[7]/text()")[0].replace("\xa0", "")
            term = tr.xpath("./td[3]/text()")[0].replace("\xa0", "")
            studyMethod = tr.xpath("./td[11]/text()")[0].replace("\xa0", "")
            dict_data = {
                "stuId": stuId,
                "className": className,
                "grade": grade,
                "classId": classId,
                "category": category,
                "score": score,
                "classNature": classNature,
                "term": term,
                "studyMethod": studyMethod,
            }
            data_list.append(dict_data)
        self._save_to_json("grade", data_list)

    def parse_empty_classroom(self, param_dict):
        api = "http://ssfw.tjut.edu.cn/ssfw/kxjs/query.do"
        data = {
            "curPageNo": "1",
            "iDisplayLength": "10",
            "totalSize": "552",
            "checkVal": "0",
            "qXnxqdm": f"{param_dict['xn']}-{param_dict['xq']}",
            "qXq": f"{param_dict['day']}",
            "qKszc": f"{param_dict['week']}",
            "qJszc": f"{param_dict['week']}",
            "qKsjc": f"{param_dict['session']}",
            "qJsjc": f"{param_dict['session']}",
            "qXaqh": "2",
            "qJxlh": "",
            "qJslx": "",
            "rsOper": "gtoeq",
            "rsCount": "",
            "qJszt": "",
            "qJsmc": ""
        }
        response = self.session.post(api, data=data)
        xpathor = etree.HTML(response.text)
        totalSize = int(xpathor.xpath(".//input[@id='totalSize']/@value")[0])
        totalPage = totalSize // 10 + 1
        page = 1
        data_list = []
        while page <= totalPage:
            tr_list = xpathor.xpath(".//tr[@class='t_con']")

            term = f"{param_dict['xn']}学年第{self.xqj_dict[int(param_dict['xq'])]}学期"
            day = f'星期{self.xqj_dict[int(param_dict["day"])]}'
            week = f"第{param_dict['week']}周"
            session = f"第{param_dict['session']}节"
            campus = "主校区"

            for tr in tr_list:
                teach_building = tr.xpath("./td[2]/span/text()")[0].replace("\xa0", "")
                classroom = tr.xpath("./td[3]/span/text()")[0].replace("\xa0", "")
                is_used = tr.xpath("./td[9]/span/text()")[0].replace("\xa0", "")
                if is_used == "可用":
                    status = True
                elif is_used == "不可用":
                    status = False
                dict_data = {
                    "term": term,
                    "day": day,
                    "week": week,
                    "session": session,
                    "campus": campus,
                    "TeachBuilding": teach_building,
                    "classroom": classroom,
                    "status": status
                }
                data_list.append(dict_data)
            page += 1

            data["curPageNo"] = page
            data["totalSize"] = totalSize
            response = self.session.post(api, data=data)
            xpathor = etree.HTML(response.text)
        self._save_to_json("classroom", data_list)

    def parse_exam(self, param_dict):
        api = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"
        data = {
            "xnxqdm": f'{param_dict["xn"]}-{param_dict["xq"]}'
        }
        response = self.session.post(api, data=data)
        xpathor = etree.HTML(response.text)
        table_list = xpathor.xpath(".//fieldset/table")
        data_list = []

        for index, table in enumerate(table_list):
            tr_list = table.xpath("./tr[@class='t_con']")

            for index_, tr in enumerate(tr_list):
                stuId = self.username
                if index == 0:
                    classId = tr.xpath("./td[2]/span/text()")[0].replace("\xa0", "")
                    className = tr.xpath("./td[3]/span/text()")[0].replace("\xa0", "")
                    status = tr.xpath("./td[last()]/span/text()")[0].replace("\xa0", "")
                    score = float(tr.xpath("./td[6]/span/text()")[0].replace("\xa0", ""))
                    location = tr.xpath("./td[8]/span/text()")[0].replace("\xa0", "")
                    examFormat = tr.xpath("./td[9]/span/text()")[0].replace("\xa0", "")
                    teacher = tr.xpath("./td[5]/span/text()")[0].replace("\xa0", "")
                    date = tr.xpath("./td[7]/span/text()")[0].replace("\xa0", "")
                    classNature = tr.xpath("./td[4]/span/text()")[0].replace("\xa0", "")
                if index > 0:
                    classId = tr.xpath("./td[2]/text()")[0].replace("\xa0", "")
                    className = tr.xpath("./td[3]/text()")[0].replace("\xa0", "")
                    status = tr.xpath("./td[last()]/text()")[0].replace("\xa0", "")
                    location = "未编排"
                    examFormat = "未编排"
                    date = "未编排"
                    if index == 1:
                        score = float(tr.xpath("./td[6]/text()")[0].replace("\xa0", ""))
                        classNature = tr.xpath("./td[4]/text()")[0].replace("\xa0", "")
                        teacher = tr.xpath("./td[5]/text()")[0].replace("\xa0", "")
                    else:
                        score = float(tr.xpath("./td[4]/text()")[0].replace("\xa0", ""))
                        teacher = "未编排"
                        classNature = "未编排"
                dict_data = {
                    "stuId": stuId,
                    "classId": classId,
                    "className": className,
                    "socre": score,
                    "location": location,
                    "examFormat": examFormat,
                    "teacher": teacher,
                    "date": date,
                    "status": status,
                    "classNature": classNature
                }
                data_list.append(dict_data)
        self._save_to_json("exam", data_list)


if __name__ == "__main__":
    username = "20200631"#input("请输入学号：").strip()
    pwd = "zky-200101040011"#input("请输入密码：").strip()
    tjlg = TJLG_University(username, pwd)
    """登录"""
    tjlg.login()
    """课程"""
    tjlg.parse_course({"xn": "2020-2021", "xq": "1"})
    # """成绩"""
    # tjlg.parse_grade({"xn": "", "xq": ""})
    # """空教室"""
    # tjlg.parse_empty_classroom({"xn": "2020-2021", "xq": "2", "day": "3", "week": "3", "session": "1"})
    # """考试"""
    # tjlg.parse_exam({"xn": "2020-2021", "xq": "2"})
