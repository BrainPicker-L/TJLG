from django import forms

class menuForm(forms.Form):
    menu_info = forms.CharField(label='蔡名/食堂名/菜品价格')