from django.db import models
from user.models import Profile
from ckeditor_uploader.fields import RichTextUploadingField


class DetailArticle(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    title = models.CharField("标题",max_length=50)
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=False)
    last_updated_time = models.DateTimeField(auto_now=False)