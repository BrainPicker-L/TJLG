from django import forms
from .models import *

class SelectForm(forms.Form):
    SELVALUE2 = tuple((i.name,str(i.id)) for i in StatusName.objects.all())
    sel_value2 = forms.CharField(max_length=15, widget=forms.widgets.Select(choices=SELVALUE2))
    reply = forms.CharField(widget=forms.Textarea)
    hidden_pk = forms.CharField(widget=forms.HiddenInput())



class SearchForm(forms.Form):
    searchtext = forms.CharField(max_length=50,label="输入工单号搜索")
    
