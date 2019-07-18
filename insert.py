import json
import os
import django
import time
os.environ['DJANGO_SETTINGS_MODULE'] = 'Tjlg.settings'
django.setup()
from gradeList.models import Guake
from all_article.models import Email
def insert_grade():
    with open('grade.txt','r') as f:
        json_data = json.loads(f.read())

    for i in json_data:
        GuakeObj = Guake()
        GuakeObj.Code = i['Code']
        GuakeObj.Name = i['Name']
        GuakeObj.Number = i['Number']
        GuakeObj.Category = i['Category']
        GuakeObj.P0_59 = i['0-59']
        GuakeObj.P60_69 = i['60-69']
        GuakeObj.P70_79 = i['70-79']
        GuakeObj.P80_89 = i['80-89']
        GuakeObj.P90_100 = i['90-100']

        GuakeObj.save()

def insert_email():
    with open('email.txt', 'r') as f:
        json_data = json.loads(f.read())
    print(len(json_data))
    for i in json_data:
        try:
            EmailObj = Email()
            EmailObj.title = i['title']
            EmailObj.ask = i["title_text"]
            EmailObj.answer = i["answer"]
            EmailObj.create_time = time.strftime("%Y-%m-%d", time.strptime(i['day'], "%Y/%m/%d"))
            EmailObj.save()
            print("ok")

        except:
            pass
insert_grade()
