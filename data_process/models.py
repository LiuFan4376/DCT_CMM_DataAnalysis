from django.db import models


# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True,verbose_name='工号')
    password = models.CharField(max_length=15,null=True,blank=True,verbose_name='密码')
