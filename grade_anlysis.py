import json
with open('a.txt','r') as f:
    list1 = f.read().split("\n")
f.close()
dict1 = {'Code':'','Name':'','Number':0,'grade_sum':0}
Code_list = []
all_dict = {}
for grade_info in list1:
    dict1 = {'Code': '', 'Name': '', 'Number': 0,'Category':'','0-59':0,'60-69':0,'70-79':0,'80-89':0,'90-100':0}
    if grade_info.split('|')[5] != '':
        Code = grade_info.split('|')[1]

        if Code not in Code_list:
            dict1['Code'] = Code
            dict1['Name'] = grade_info.split('|')[2]
            dict1['Number'] += 1
            dict1['Category'] = grade_info.split('|')[3]

            if int(grade_info.split('|')[4]) < 60:
                dict1["0-59"] += 1
            elif 60<=int(grade_info.split('|')[4])<=69:
                dict1["60-69"] += 1
            elif 70<=int(grade_info.split('|')[4])<=79:
                dict1["70-79"] += 1
            elif 80<=int(grade_info.split('|')[4])<=89:
                dict1["80-89"] += 1
            elif 90<=int(grade_info.split('|')[4])<=100:
                dict1["90-100"] += 1
            all_dict[Code] = dict1
            Code_list.append(Code)
        else:
            all_dict[Code]["Number"] += 1
            if int(grade_info.split('|')[4]) < 60:
                all_dict[Code]["0-59"] += 1
            elif 60<=int(grade_info.split('|')[4])<=69:
                all_dict[Code]["60-69"] += 1
            elif 70<=int(grade_info.split('|')[4])<=79:
                all_dict[Code]["70-79"] += 1
            elif 80<=int(grade_info.split('|')[4])<=89:
                all_dict[Code]["80-89"] += 1
            elif 90<=int(grade_info.split('|')[4])<=100:
                all_dict[Code]["90-100"] += 1
new_lists = []
for k,v in all_dict.items():
    if v["Number"]>=5:
        all_dict[k]['0-59'] = '{:.2%}'.format(v["0-59"]/v["Number"])
        all_dict[k]['60-69'] = '{:.2%}'.format(v["60-69"] / v["Number"])
        all_dict[k]['70-79'] = '{:.2%}'.format(v["70-79"] / v["Number"])
        all_dict[k]['80-89'] = '{:.2%}'.format(v["80-89"] / v["Number"])
        all_dict[k]['90-100'] = '{:.2%}'.format(v["90-100"] / v["Number"])
        new_lists.append(all_dict[k])
        print(all_dict[k])
with open('grade.txt','w') as f:

    f.write(json.dumps(new_lists))
f.close()