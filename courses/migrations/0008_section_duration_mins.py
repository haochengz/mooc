# Generated by Django 2.0.2 on 2018-05-04 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20180504_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='duration_mins',
            field=models.IntegerField(default=0, verbose_name='时长'),
        ),
    ]
