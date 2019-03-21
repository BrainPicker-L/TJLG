f = open('memu.txt.utf8')

menu_list = f.read().split("\n")

all_list = []
list1 = []
list2 = []
for i in menu_list:
    if "食堂" in i:
        if list1 != []:
            list1.append(list2)
            all_list.append(list1)
            list2 = []
        list1 = []
    elif "窗口" in i:
        if list2 != []:
            list1.append(list2)
        list2 = ["",[]]
        list2[0] = i
    else:
        list2[1].append(i)
list1.append(list2)
all_list.append(list1)

