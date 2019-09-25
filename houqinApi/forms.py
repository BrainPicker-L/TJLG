from django import forms
from .models import *

class SelectForm(forms.Form):
    SELVALUE = tuple((i.name,str(i.id)) for i in RepairMan.objects.all())
    SELVALUE2 = tuple((i.name,str(i.id)) for i in StatusName.objects.all())
    sel_value = forms.CharField(max_length=15, widget=forms.widgets.Select(choices=SELVALUE))
    sel_value2 = forms.CharField(max_length=15, widget=forms.widgets.Select(choices=SELVALUE2))
    hidden_pk = forms.CharField(widget=forms.HiddenInput())