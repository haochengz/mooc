# Generated by Django 2.0.2 on 2018-05-03 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180421_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tag',
            field=models.CharField(default='', max_length=10, verbose_name='课程类别'),
        ),
    ]
