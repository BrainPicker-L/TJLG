from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url("get_start_school_day", views.get_start_school_day,name="get_start_school_day"),
    url("", views.info, name="info"),

]