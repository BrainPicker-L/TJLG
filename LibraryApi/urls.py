from django.conf.urls import url
from . import views


urlpatterns = [
    url("", views.library, name="library")
]