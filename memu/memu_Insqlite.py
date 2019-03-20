f = open('memu.txt')
all_list = f.read().split("\n")
dict1 = {}
for i in all_list:
    if "食堂" in i:
        dict1["diningRoom"] = i
    elif "窗口" in i:
        dict1["winNum"] = i
    else:
        dict1["namePrice"] = i
        print(dict1)
