import requests
from lxml import etree
import datetime
import logging
headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'Tjlg.settings'
django.setup()

from all_article.models import Article
from user.models import Profile

def get_title_list():
        title_list = []
        articles = Article.objects.all()
        for article in articles:
                title_list.append(article.title)
        return title_list


#拿到天津理工教务通知文章
def get_notice():
        url = "http://www.tjut.edu.cn/index/xngg.htm"
        r = requests.get(url=url,headers=headers)
        html = r.content.decode("utf-8")

        selector = etree.HTML(html)
        tr_list = selector.xpath('//table[@class="winstyle130278"]/tr')
        title_list = get_title_list()
        for tr in tr_list:
                create_time = tr.xpath('./td[3]/span/text()')
                if create_time!=[]:
                        create_time = create_time[0].replace("\xa0","").replace("/","-")
                        title = tr.xpath('./td[2]/a/text()')[0].replace(" ","").replace("\n","")
                        if str(datetime.date.today()) == create_time and title not in title_list:  #str(datetime.date.today())
                        #if "2018-12-11" == create_time:
                                articleObj = Article()
                                detail_url = "http://www.tjut.edu.cn" + tr.xpath('./td[2]/a/@href')[0][2:]
                                detail_r = requests.get(url=detail_url,headers=headers)
                                detail_html = detail_r.content.decode("utf-8")
                                detail_selector = etree.HTML(detail_html)

                                articleObj.author = Profile.objects.filter(user__username="教务快讯")[0]
                                articleObj.title = title
                                excerpt = "".join(detail_selector.xpath('//div[@class="Section0"]//text()'))
                                if len(excerpt)>200:
                                        excerpt = excerpt[:200]
                                excerpt = excerpt + "...（详情见教务%s）" % detail_url
                                articleObj.excerpt = "【{title}】".format(title=title) + "\n" +excerpt
                                cur = datetime.datetime.now()
                                articleObj.created_time = "%s-%s-%s %s:%s" % (cur.year, cur.month, cur.day, cur.hour, cur.minute)
                                articleObj.last_updated_time = "%s-%s-%s %s:%s" % (cur.year, cur.month, cur.day, cur.hour, cur.minute)
                                articleObj.save()


def get_news():
        urls = ["http://news.tjut.edu.cn/yw1.htm","http://news.tjut.edu.cn/yw.htm"]
        for url in urls:
                r = requests.get(url=url,headers=headers)
                html = r.content.decode("utf-8")

                selector = etree.HTML(html)
                tr_list = selector.xpath('//table[@class="winstyle52564"]/tr[@height="29"]')
                title_list = get_title_list()

                for tr in tr_list:
                        create_time = tr.xpath('./td[3]/span/text()')
                        if create_time != []:
                                create_time = create_time[0].replace("\xa0", "").replace("/", "-")
                                title = tr.xpath('./td[2]/a/text()')[0].replace(" ", "").replace("\n", "")
                                if str(datetime.date.today()) == create_time and title not in title_list:  # str(datetime.date.today())
                                        articleObj = Article()
                                        detail_url = "http://news.tjut.edu.cn/" + tr.xpath('./td[2]/a/@href')[0]
                                        detail_r = requests.get(url=detail_url,headers=headers)
                                        detail_html = detail_r.content.decode("utf-8")
                                        detail_selector = etree.HTML(detail_html)

                                        articleObj.author = Profile.objects.filter(user__username="教务快讯")[0]
                                        articleObj.title = title

                                        excerpt = "\n".join(detail_selector.xpath('//div[@class="v_news_content"]/p[not(@style="text-align: center;")]//text()'))
                                        if len(excerpt) > 200:
                                                excerpt = excerpt[:200]
                                        excerpt = excerpt + "...（详情见教务%s）" % detail_url
                                        articleObj.excerpt = "【{title}】".format(title=title) + "\n" + excerpt
                                        cur = datetime.datetime.now()
                                        articleObj.created_time = "%s-%s-%s %s:%s" % (cur.year, cur.month, cur.day, cur.hour, cur.minute)
                                        articleObj.last_updated_time = "%s-%s-%s %s:%s" % (cur.year, cur.month, cur.day, cur.hour, cur.minute)
                                        articleObj.save()



if __name__=="__main__":
        get_notice()
        get_news()
