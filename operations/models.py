from django.db import models
from django.utils import timezone

from users.models import UserProfile
from courses.models import Course


class UserConsult(models.Model):
    name = models.CharField(verbose_name="咨询者名称", max_length=20)
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    course_name = models.CharField(verbose_name="咨询课程", max_length=50)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return None


class UserMessage(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    message = models.CharField(verbose_name="消息内容", max_length=500)
    is_read = models.BooleanField(verbose_name="是否已读", default=False)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return None


class CourseComment(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="评论", max_length=500)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return None


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = ""
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return None


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name="收藏数据id", default=0)
    fav_type = models.IntegerField(verbose_name="收藏类型", default=1, choices=(
        (1, ""),
        (2, ""),
        (3, ""),
    ))
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return None
