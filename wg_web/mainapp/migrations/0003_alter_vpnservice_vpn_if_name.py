# Generated by Django 4.0.6 on 2022-07-13 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_vpnservice_vpn_if_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpnservice',
            name='vpn_if_name',
            field=models.CharField(default='wg0', max_length=50, verbose_name='VPN Service interface name'),
        ),
    ]
