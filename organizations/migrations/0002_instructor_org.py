# Generated by Django 2.0.2 on 2018-04-16 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='org',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organizations.Org', verbose_name='所属机构'),
        ),
    ]
