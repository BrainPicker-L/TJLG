from django.conf.urls import url
from . import views

urlpatterns = [
    url("", views.top_article, name="top_article")
]