# Generated by Django 2.0.2 on 2018-04-16 04:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='接收邮箱')),
                ('verify_type', models.CharField(choices=[('register', ''), ('forget', '')], max_length=10, verbose_name='验证类型')),
                ('send_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证',
                'verbose_name_plural': '邮箱验证',
            },
        ),
    ]
