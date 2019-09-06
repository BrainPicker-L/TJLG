"""Tjlg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.conf.urls.static import static
from Tjlg import views
from all_article.views import *
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path("library/",include("LibraryApi.urls")),
    path("info/",include("InfoApi.urls")),
    path("top_article/",include("top_article.urls")),
    path("detail_article/",include("detail_article.urls")),
    path("manage_detail/",views.manage_detail,name="manage_detail"),
    path("edit_detail_article/<int:article_pk>",views.edit_detail_article,name="edit_detail_article"),
    path('login/', views.login, name='login'),
    path('register_user/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('manage_article',views.manage_article,name = 'manage_article'),
    path('edit_article/<int:article_pk>',views.edit_article,name = 'edit_article'),
    path('tests',include("Tests.urls")),
    path('delete_article/<int:article_pk>',views.delete_article,name="delete_article"),
    path('delete_detail_article/<int:article_pk>',views.delete_detail_article,name="delete_detail_article"),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('phone_detail_article/<int:article_pk>',views.phone_detail_article,name="phone_detail_article"),
    path('all_article',article_list_shetuan, name="article_list_shetuan"),
    path('all_article_jiaowu',article_list_jiaowu, name="article_list_jiaowu"),
    path('start_school_day',views.start_school_day,name='start_school_day'),
    path('lecture',views.lecture,name="lecture"),
    path('menu',views.menu,name="menu"),
    path('menu_list',views.menu_list,name="menu_list"),
    path('guake',views.guake,name="guake"),
    path('psf',views.psf,name="psf"),
    path('personal_flag',views.personal_flag,name="personal_flag"),
    path('email',views.email,name='email'),
    path('searchemail',views.emailSearch,name='emailSearch'),
    path('emaildetail',views.emaildetail,name='emaildetail'),
    path('getarticle',views.getarticle,name='getarticle'),
    path('jspj',views.jspj,name='jspj'),
    path('useraction',views.useraction,name='useraction'),
    path('comment_action',views.comment_action,name='comment_action'),
    path('personal_action',views.personal_action,name='personal_action'),
    path('change_like_num_action',views.change_like_num_action,name='change_like_num_action'),
    path('change_like_num_comment',views.change_like_num_comment,name='change_like_num_comment'),
    path('school_life',views.school_life,name='school_life'),
    path('TJLG_school_life',views.TJLG_school_life,name='TJLG_school_life'),
    path('delete_action',views.delete_action,name='delete_action'),
    path('delete_commit',views.delete_commit,name='delete_commit'),
    path('ahu_advert',views.ahu_advert,name='ahu_advert'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
