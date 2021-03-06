from django.db import models
from django.utils import timezone

from organizations.models import Org, Instructor


class Course(models.Model):
    name = models.CharField(verbose_name="课程名", max_length=30)
    teacher = models.ForeignKey(Instructor, verbose_name="讲师", default=None,
                                on_delete=models.CASCADE, null=True, blank=True)
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
    category = models.CharField(verbose_name="课程类别", max_length=20, default="")
    hits = models.IntegerField(verbose_name="点击量", default=0)
    org = models.ForeignKey(Org, verbose_name="所属机构", on_delete=models.CASCADE, default=None)
    tag = models.CharField(verbose_name="标签", max_length=20, default="")
    tips = models.CharField(verbose_name="讲师提示", max_length=200, default="")
    notice = models.CharField(verbose_name="学前须知", max_length=200, default="")
    is_ad = models.BooleanField(verbose_name="是否是广告客户", default=False)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_chapter_nums(self):
        return self.chapter_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_students_nums(self):
        return self.usercourse_set.all().count()

    def get_course_lesson(self):
        return self.chapter_set.all()

    def get_degree(self):
        if self.degree == "junior":
            return "初级"
        elif self.degree == "senior":
            return "中级"
        elif self.degree == "expert":
            return "高级"


class Chapter(models.Model):
    course = models.ForeignKey(Course, verbose_name="所属课程", on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name="章节名", max_length=30)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "章"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.section_set.all()


class Section(models.Model):
    chapter = models.ForeignKey(Chapter, verbose_name="所属章节", on_delete=models.CASCADE, default=None)
    name = models.CharField(verbose_name="小节名", max_length=30, default="")
    url = models.CharField(verbose_name="视频地址", max_length=300, default="")
    duration_mins = models.IntegerField(verbose_name="时长", default=0)
    add_time = models.DateTimeField(verbose_name="添加时间", default=timezone.now)

    class Meta:
        verbose_name = "小节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def __str__(self):
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

    def __str__(self):
        return self.name
