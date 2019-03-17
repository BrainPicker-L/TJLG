from django.urls import path
from . import views

# start with blog
urlpatterns = [
    path('<int:article_pk>', views.detail_article, name="detail_article"),
]