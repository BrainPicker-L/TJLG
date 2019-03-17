from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField("用户头像",upload_to='img')

    def __str__(self):
        return '%s'%(self.user.username)