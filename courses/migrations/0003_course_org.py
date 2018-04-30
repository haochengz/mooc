# Generated by Django 2.0.2 on 2018-04-30 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_org_course_nums'),
        ('courses', '0002_auto_20180416_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='org',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organizations.Org', verbose_name='所属机构'),
        ),
    ]