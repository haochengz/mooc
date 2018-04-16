
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=(("male", "男"), ("female", "女")), default="male", max_length=6)
    address = models.CharField(verbose_name="地址", max_length=100, default="")
    mobile = models.CharField(verbose_name="手机号码", max_length=11, null=True, blank=True)
    image = models.ImageField(verbose_name="头像", upload_to="media/image/%Y/%m", default="media/image/default.png")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

