f = open('memu.txt.utf8')

menu_list = f.read().split("\n")

all_list = []
dict1 = {}
for i in menu_list:
    if "食堂" in i:
        if dict1 != {}:
            all_list.append(dict1)
        dict1 = {}
    elif "窗口" in i:
        dict1[i] = []
        win_name = i
    else:
        dict1[win_name].append(i)

print(all_list)