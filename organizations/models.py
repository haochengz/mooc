from django.db import models
from django.utils import timezone


class Location(models.Model):
    name = models.CharField(verbose_name="城市名", max_length=20)
    desc = models.CharField(verbose_name="城市描述", max_length=200)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Org(models.Model):
    name = models.CharField(verbose_name="机构名称", max_length=50)
    desc = models.TextField(verbose_name="机构描述")
    hits = models.IntegerField(verbose_name="点击量", default=0)
    favorite_nums = models.IntegerField(verbose_name="收藏数", default=0)
    image = models.ImageField(verbose_name="封面图", upload_to="media/org/%Y/%m")
    address = models.CharField(verbose_name="地址", max_length=200)
    category = models.CharField(verbose_name="类别",
                                choices=(("personal", "个人"), ("vocational", "职业培训"), ("college", "高校"),),
                                max_length=10, default="personal")
    enrolled_nums = models.IntegerField(verbose_name="注册学生人数", default=0)
    course_nums = models.IntegerField(verbose_name="开放课程数量", default=0)
    located = models.ForeignKey(Location, verbose_name="位于", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "机构"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Instructor(models.Model):
    org = models.ForeignKey(Org, verbose_name="所属机构", on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name="教师名称", max_length=50)
    hits = models.IntegerField(verbose_name="点击量", default=0)
    favorite_nums = models.IntegerField(verbose_name="收藏数", default=0)
    employed = models.CharField(verbose_name="就职于", max_length=50)
    position = models.CharField(verbose_name="职位", max_length=50)
    service_len = models.IntegerField(verbose_name="工作年限", default=0)
    characteristics = models.CharField(verbose_name="教学特点", max_length=500)
    image = models.ImageField(verbose_name="头像", upload_to="media/instructor/%Y/%m", max_length=200, default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
