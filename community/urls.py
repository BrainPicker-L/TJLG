from django.urls import path
from . import views

# start with blog
urlpatterns = [

    path('useraction', views.useraction, name='useraction'),
    path('comment_action', views.comment_action, name='comment_action'),
    path('personal_action', views.personal_action, name='personal_action'),
    path('change_like_num_action', views.change_like_num_action, name='change_like_num_action'),
    path('change_like_num_comment', views.change_like_num_comment, name='change_like_num_comment'),
    path('delete_action', views.delete_action, name='delete_action'),
    path('delete_comment', views.delete_comment, name='delete_comment'),
    path('notice_lst',views.notice_lst,name='notice_lst'),
    path('get_unread_num',views.get_unread_num,name='get_unread_num'),
    path('get_author_id',views.get_author_id,name='get_author_id'),
    path('uoload_img',views.upload_img,name='upload_img')
]
