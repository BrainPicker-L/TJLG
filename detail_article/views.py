from django.shortcuts import render
from .models import *
# Create your views here.
def detail_article(request,article_pk):
    context = {}
    context['article'] = DetailArticle.objects.get(pk=article_pk)
    return render(request, 'detail_article.html', context)

