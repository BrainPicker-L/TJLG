from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('', views.houqin_home, name="houqin_home"),
    path('/gongdan/<int:gd_pk>', views.houqin_detail,name="houqin_detail"),
    path('/add_gongdan',views.add_gongdan,name='add_gongdan'),
    path('/person_gongdan_status',views.person_gongdan_status,name='person_gongdan_status')
]