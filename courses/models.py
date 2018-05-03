from django.db import models
from django.utils import timezone

from organizations.models import Org


class Course(models.Model):
    name = models.CharField(verbose_name="课程名", max_length=30)
    desc = models.CharField(verbose_name="简介", max_length=500)
    detail = models.TextField(verbose_name="详情")
    degree = models.CharField(verbose_name="难度", choices=(
        ("junior", "初级"),
        ("senior", "中级"),
        ("expert", "高级"),
    ), max_length=10)
    duration_mins = models.IntegerField(verbose_name="总时长", default=0)
    enrolled_nums = models.IntegerField(verbose_name="注册人数", default=0)
    favorite_nums = models.IntegerField(verbose_name="收藏人数", default=0)
    image = models.ImageField(verbose_name="封面图片", upload_to="media/courses/%Y/%m")
    hits = models.IntegerField(verbose_name="点击量", default=0)
    org = models.ForeignKey(Org, verbose_name="所属机构", on_delete=models.CASCADE, default=None)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name="章节名", max_length=30)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "章"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Section(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name="所属章节", on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name="小节名", max_length=30)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "小节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name="资源名", max_length=30)
    path = models.FileField(verbose_name="资源链接", upload_to="media/courses/resourses/%Y/%m")
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
