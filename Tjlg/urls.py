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
from all_article.views import article_list
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
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('manage_article',views.manage_article,name = 'manage_article'),
    path('edit_article/<int:article_pk>',views.edit_article,name = 'edit_article'),
    path('tests',include("Tests.urls")),
    path('delete_article/<int:article_pk>',views.delete_article,name="delete_article"),
    path('delete_detail_article/<int:article_pk>',views.delete_detail_article,name="delete_detail_article"),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('phone_detail_article/<int:article_pk>',views.phone_detail_article,name="phone_detail_article"),
    path('all_article/',article_list, name="article_list"),
    path('start_school_day',views.start_school_day,name='start_school_day')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
