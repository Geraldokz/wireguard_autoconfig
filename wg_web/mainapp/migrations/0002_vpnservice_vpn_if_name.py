# Generated by Django 4.0.6 on 2022-07-12 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vpnservice',
            name='vpn_if_name',
            field=models.CharField(default='eth0', max_length=50, verbose_name='VPN Service interface name'),
        ),
    ]
