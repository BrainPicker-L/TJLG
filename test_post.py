import requests


data = {

    'sno' :'Y21614010',
    'name' :'子哲',
    'phonenum' :'18815516404',
    'pos' :'食堂aaa',
    'abletime' :'全天aaa',
    'excerpt' :'桌子坏了aaa',
}

res =  requests.post('http://127.0.0.1:8000/houqin/add_gongdan',data=data)
print(res.text)