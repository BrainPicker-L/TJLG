
import os,django,sys
sys.path.append('/home/TJLG')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tjlg.settings")# project_name 项目名称
django.setup()
from menuApi.models import Menu
f = open('memu.txt.utf8')
all_list = f.read().split("\n")

for i in all_list:
    menu_info = Menu()
    if "食堂" in i:
        diningRoom = i
    elif "窗口" in i:
        winNum = i
    else:
        menu_info.diningRoom = diningRoom
        menu_info.winNum = winNum
        menu_info.namePrice = i
        menu_info.save()
