from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.serializers import serialize,deserialize
from Tjlg.settings import HOSTS
from .models import *
def top_article(request):
    if request.method == "GET":
        queryset = top_article_model.objects.all()
        context_list = []

        for i in queryset:
            dict1 = {}
            dict1['title'] = i.title
            dict1['image'] = HOSTS+i.img.url
            dict1['detail'] = i.detail
            context_list.append(dict1)
        context_list_json = json.dumps(context_list)
        return HttpResponse(context_list_json)