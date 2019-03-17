from django import forms

class AddForm(forms.Form):
    a = forms.CharField(label='书名')
    b = forms.CharField(label='页码')