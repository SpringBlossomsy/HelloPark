# Generated by Django 2.2.2 on 2019-06-25 13:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.BooleanField(default=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('note', models.CharField(blank=True, max_length=1024)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='park.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='UserPrakSeat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=12)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=12)),
                ('pioaddress', models.CharField(blank=True, max_length=512)),
                ('note', models.CharField(blank=True, max_length=2048)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time02', models.BooleanField(default=False)),
                ('time24', models.BooleanField(default=False)),
                ('time46', models.BooleanField(default=False)),
                ('time68', models.BooleanField(default=False)),
                ('time810', models.BooleanField(default=False)),
                ('time1012', models.BooleanField(default=False)),
                ('time1214', models.BooleanField(default=False)),
                ('time1416', models.BooleanField(default=False)),
                ('time1618', models.BooleanField(default=False)),
                ('time1820', models.BooleanField(default=False)),
                ('time2022', models.BooleanField(default=False)),
                ('time2224', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='park.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=False)),
                ('note', models.CharField(blank=True, max_length=1024)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_source', to='park.UserProfile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='park.UserProfile')),
            ],
        ),
    ]
