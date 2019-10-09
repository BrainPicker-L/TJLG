import requests

for i in range(10):
    data = {
        'sno' :'Y21614010',
        'name' :'刘子哲',
        'excerpt' :'空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调空调',
    }
    #
    res =  requests.post('http://127.0.0.1:8000/houqin/add_gongdan',data=data)
    print(res.text)
