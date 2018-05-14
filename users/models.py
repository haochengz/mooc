
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=20, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=(("male", "男"), ("female", "女")), default="male", max_length=6)
    address = models.CharField(verbose_name="地址", max_length=100, default="")
    mobile = models.CharField(verbose_name="手机号码", max_length=11, null=True, blank=True)
    tag = models.CharField(verbose_name="课程类别", max_length=10, default="")
    # TODO: What did this tag field for?
    image = models.ImageField(verbose_name="头像", upload_to="media/image/%Y/%m", default="media/image/default.png")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        from operations.models import UserMessage
        return UserMessage.objects.filter(user=self, is_read=False).count()


class EmailVerify(models.Model):
    code = models.CharField(verbose_name="验证码", max_length=32, unique=True)
    email = models.EmailField(verbose_name="接收邮箱", max_length=50)
    verify_type = models.CharField(verbose_name="验证类型", choices=(("register", ""), ("forget", "")), max_length=10)
    send_time = models.DateTimeField(verbose_name="发送时间", default=timezone.now)

    class Meta:
        verbose_name = "邮箱验证"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.email


class Banner(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    image = models.ImageField(verbose_name="图片路径", upload_to="media/banner/%Y/%m", max_length=100)
    url = models.URLField(verbose_name="打开地址", max_length=200)
    index = models.IntegerField(verbose_name="播放顺序", default=10000)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
