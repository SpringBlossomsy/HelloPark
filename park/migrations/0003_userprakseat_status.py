# Generated by Django 2.2.2 on 2019-06-25 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0002_order_userprakseat_walletdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprakseat',
            name='status',
            field=models.CharField(default='0', max_length=32),
        ),
    ]
