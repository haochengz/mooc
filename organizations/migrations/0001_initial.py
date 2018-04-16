# Generated by Django 2.0.2 on 2018-04-16 07:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='教师名称')),
                ('hits', models.IntegerField(default=0, verbose_name='点击量')),
                ('favorite_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('employed', models.CharField(max_length=50, verbose_name='就职于')),
                ('position', models.CharField(max_length=50, verbose_name='职位')),
                ('service_len', models.IntegerField(default=0, verbose_name='工作年限')),
                ('characteristics', models.CharField(max_length=500, verbose_name='教学特点')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '教师',
                'verbose_name_plural': '教师',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='城市名')),
                ('desc', models.CharField(max_length=200, verbose_name='城市描述')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '城市',
                'verbose_name_plural': '城市',
            },
        ),
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='机构名称')),
                ('desc', models.TextField(verbose_name='机构描述')),
                ('hits', models.IntegerField(default=0, verbose_name='点击量')),
                ('favorite_nums', models.IntegerField(default=0, verbose_name='收藏数')),
                ('image', models.ImageField(upload_to='media/org/%Y/%m', verbose_name='封面图')),
                ('address', models.CharField(max_length=200, verbose_name='地址')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('located', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Location', verbose_name='位于')),
            ],
            options={
                'verbose_name': '机构',
                'verbose_name_plural': '机构',
            },
        ),
    ]
