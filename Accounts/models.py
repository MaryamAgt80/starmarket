from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, verbose_name='نام')
    email = models.CharField(max_length=200, verbose_name='ایمیل')
    password = models.CharField(max_length=100, verbose_name='رمز')
    active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی')
    is_active = models.BooleanField(default=False,verbose_name='فعال/غیرفعال')
    job=models.CharField(max_length=100,blank=True,null=True,default='',verbose_name='شغل')
    natiional_code=models.CharField(max_length=10,blank=True,null=True,default='',verbose_name='کد ملی')
    lname=models.CharField(max_length=200,blank=True,null=True,default='', verbose_name='نام خانوادگی')
    re_email= models.CharField(max_length=200,blank=True,null=True,default='', verbose_name='ایمیل جایگزین')

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'
    def __str__(self):
        return self.username


