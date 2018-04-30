# Generated by Django 2.0.2 on 2018-04-30 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='所属课程'),
        ),
        migrations.AlterField(
            model_name='section',
            name='chapter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.Chapter', verbose_name='所属章节'),
        ),
    ]
