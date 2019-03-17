from django import forms

class InfoForm(forms.Form):
    user = forms.CharField(label='学号')
    password = forms.CharField(label='密码')
    choice = forms.CharField(label='选择')