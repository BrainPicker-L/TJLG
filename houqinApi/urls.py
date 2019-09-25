from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('', views.houqin_home, name="houqin_home"),
    path('gongdan/<int:gd_pk>', views.houqin_detail,name="houqin_detail"),
]