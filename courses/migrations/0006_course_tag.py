# Generated by Django 2.0.2 on 2018-05-04 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20180503_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=20, verbose_name='标签'),
        ),
    ]