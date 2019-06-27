# Generated by Django 2.2.2 on 2019-06-27 10:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0007_userprakseat_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprakseat',
            name='start_time',
        ),
        migrations.AddField(
            model_name='order',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
