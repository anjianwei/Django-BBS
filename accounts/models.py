from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    username = models.ForeignKey(User, related_name='User_Profiles', on_delete=models.CASCADE)
    avatar = models.FileField(upload_to='avatar', blank=True,null=True, verbose_name='头像')
