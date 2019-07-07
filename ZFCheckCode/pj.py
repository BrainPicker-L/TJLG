# -*-coding:utf-8-*-
import os
import re
from lxml import etree
import requests
import sys
import imp
from ZFCheckCode.ZFCheckCode import recognizer
imp.reload(sys)
FILE_PATH =os.path.abspath(os.path.dirname(__file__))
os.chdir(FILE_PATH)

class AhuPj:
    def __init__(self,studentnumber,password):
        self.s = requests.session()
        self.studentnumber = studentnumber
        self.password = password
        self.li = ''
        self.li_kc_name = ''
        self.xh = ''
    def identify(self):
        code = recognizer.recognize_checkcode('./code.png')
        print(code)
        return code
    # 匹配正确评教链接
    def myfilter(self,L):
        if (L.find('xsjxpj.aspx')):
            return False
        else:
            return True


    def getInfor(self,response, xpath):
        content = response.content.decode('gb2312')  # 网页源码是gb2312要先解码
        selector = etree.HTML(content)
        infor = selector.xpath(xpath)
        return infor


    # 评教并保存
    def doEvaluate(self,response, index, head):
        print('正在评价' + self.li_kc_name[index] + '...')
        response = self.s.post('http://jw2.ahu.cn/' + self.li[index], data=None, headers=head)
        __VIEWSTATE = self.getInfor(response, '//*[@name="__VIEWSTATE"]/@value')
        __VIEWSTATEGENERATOR = self.getInfor(response, '//*[@name="__VIEWSTATEGENERATOR"]/@value')
        post_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            'pjkc': self.xh[index][:-4],
            'pjxx': '',
            'txt1': '',
            'TextBox1': '0',
            'Button1': u'保  存'.encode('gb2312')
        }
        print(post_data['pjkc'])
        for i in range(2, 9):
            if i == 2:
                post_data.update({'DataGrid1:_ctl' + str(i) + ':JS1': u'良好'.encode('gb2312')})
            else:
                post_data.update({'DataGrid1:_ctl' + str(i) + ':JS1': u'优秀'.encode('gb2312')})
                post_data.update({'DataGrid1:_ctl' + str(i) + ':txtjs1': ''})
        response = self.s.post('http://jw2.ahu.cn/' + self.li[index], data=post_data, headers=head)


    def run(self):
        try:
            # studentnumber = input('学号：')
            # password = input('密码：')
            index = 0
            url = "http://jw2.ahu.cn/default2.aspx"
            userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
            response = self.s.get(url)
            # 使用xpath获取__VIEWSTATE，__VIEWSTATEGENERATOR
            selector = etree.HTML(response.content)
            __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
            __VIEWSTATEGENERATOR = selector.xpath('//*[@id="form1"]/input/@value')[1]
            # 获取验证码并下载到本地
            imgUrl = "http://jw2.ahu.cn/CheckCode.aspx"
            imgresponse = self.s.get(imgUrl, stream=True)
            image = imgresponse.content
            DstDir = os.getcwd() + "\\"

            try:
                with open("./code.png", "wb") as jpg:
                    jpg.write(image)
            except IOError:
                print("IO Error\n")

            # 手动输入验证码
            code = self.identify()
            # 构建post数据
            RadioButtonList1 = u"学生".encode('gb2312', 'replace')
            data = {
                "RadioButtonList1": RadioButtonList1,
                "__VIEWSTATE": __VIEWSTATE,
                "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
                "txtUserName": self.studentnumber,
                "TextBox2": self.password,
                "txtSecretCode": code,
                "Button1": "",
                "lbLanguage": ""
            }
            headers = {
                "User-Agent": userAgent,
            }
            # 登陆教务系统
            response = self.s.post(url, data=data, headers=headers)
            # 获取学生基本信息
            try:
                text = self.getInfor(response, '//*[@id="xhxm"]/text()')[0]
            except IndexError:
                print('验证码或密码错误！请重试')
                return "error"
            if (text != None):
                studentname = text
                print('成功进入教务系统！')
                print(studentname)
            # 获取评教链接及课程名
            self.li = self.getInfor(response, '//*[@class="sub"]/li/a/@href')
            self.li = self.li[4:]
            self.li_kc_name = self.getInfor(response, '//*[@class="sub"]/li/a/text()')
            self.li_kc_name = self.li_kc_name[4:]
            self.li = list(filter(self.myfilter, self.li))
            self.li_kc_name = self.li_kc_name[:len(self.li)]
            self.xh = []
            for i in range(len(self.li)):
                self.xh.append(self.li[i][17:50])
            head = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep - alive',
                'Host': 'jw2.ahu.cn',
                'Referer': 'http://jw2.ahu.cn/xs_main.aspx?xh=' + self.studentnumber,
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': userAgent
            }
            try:
                response = self.s.post('http://jw2.ahu.cn/' + self.li[0], data=None, headers=head)
                # 根据课程数量进行评教并保存
                for i in range(len(self.li)):
                    self.doEvaluate(response, index, head)
                    index = index + 1
                # 提交
                response = self.s.post('http://jw2.ahu.cn/' + self.li[index - 1], data=None, headers=head)
                __VIEWSTATE = self.getInfor(response, '//*[@name="__VIEWSTATE"]/@value')
                __VIEWSTATEGENERATOR = self.getInfor(response, '//*[@name="__VIEWSTATEGENERATOR"]/@value')
                post_data = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': __VIEWSTATE,
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    'pjkc': self.xh[index - 1],
                    'pjxx': '',
                    'txt1': '',
                    'TextBox1': '0',
                    'Button2': u'提  交'.encode('gb2312')
                }
                response = self.s.post('http://jw2.ahu.cn/' + self.li[index - 1], data=post_data, headers=head)
                print('评教完成！请登陆教务系统查看结果！')
                print('        *********************感谢使用*********************')
                return "1"
            except IndexError:
                return "0"
        except:
            return "error"

if __name__ == '__main__':
    a = AhuPj('Y2161401','sm3297297')
    print(a.run())