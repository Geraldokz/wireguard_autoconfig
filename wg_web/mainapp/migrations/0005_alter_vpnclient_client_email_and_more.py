# Generated by Django 4.0.6 on 2022-07-13 11:45

import django.core.validators
from django.db import migrations, models
import mainapp.services.vpn_services.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_vpndevice_private_ip_alter_vpnserver_public_ip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vpnclient',
            name='client_email',
            field=models.CharField(max_length=255, validators=[django.core.validators.EmailValidator()], verbose_name='VPN Client email'),
        ),
        migrations.AlterField(
            model_name='vpndevice',
            name='private_key',
            field=models.CharField(default='oD+NUdbl3TgjSKCIezK2al2n5gpbC/WH+SwnzTv1b1Y=', max_length=44, verbose_name='VPN Device privkey'),
        ),
        migrations.AlterField(
            model_name='vpndevice',
            name='public_key',
            field=models.CharField(default='GR3Zeg8HB9iW69/oJVMnfAWV7GhuFqtoRkfHlzc01V4=', max_length=44, verbose_name='VPN Device pubkey'),
        ),
        migrations.AlterField(
            model_name='vpnservice',
            name='private_key',
            field=models.CharField(default='yPYHQ6vHaamwskIAhwwRULxS36PAoW26jbbBqefbHmw=', max_length=44, verbose_name='VPN Service privkey'),
        ),
        migrations.AlterField(
            model_name='vpnservice',
            name='public_key',
            field=models.CharField(default='8PqpeMlH2xIUlq4ZqR+wdkiCJTdkioqoGpz7koWoBmg=', max_length=44, verbose_name='VPN Service pubkey'),
        ),
        migrations.AlterField(
            model_name='vpnservice',
            name='vpn_network',
            field=models.CharField(max_length=18, validators=[mainapp.services.vpn_services.validators.validate_network], verbose_name='VPN Service network'),
        ),
    ]