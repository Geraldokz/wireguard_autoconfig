from django.core.validators import validate_ipv4_address, validate_email
from django.db import models
from django.shortcuts import reverse

from mainapp.services.wg_keys import generate_keys
from mainapp.services.vpn_services.validators import validate_network


class VPNServer(models.Model):
    """VPN Server model"""
    hostname = models.CharField(max_length=255, verbose_name='Hostname')
    public_ip = models.CharField(max_length=15, verbose_name='Server IP', validators=[validate_ipv4_address])
    if_name = models.CharField(max_length=50, verbose_name='Eth interface name')

    def __str__(self):
        return f'{self.hostname}'


# TO DO
# 1. Replace keys generating logic to save method
# 2. Make auto generate private ip field with first address in vpn_network
class VPNService(models.Model):
    """VPN Service model"""
    PRIVATE_KEY, PUBLIC_KEY = generate_keys()

    service_name = models.CharField(max_length=255, verbose_name='VPN Service name')
    vpn_network = models.CharField(max_length=18, verbose_name='VPN Service network', validators=[validate_network])
    vpn_port = models.IntegerField(verbose_name='VPN port')
    private_ip = models.CharField(max_length=15, verbose_name='VPN Service ip', validators=[validate_ipv4_address])
    vpn_if_name = models.CharField(max_length=50, verbose_name='VPN Service interface name', default='wg0')
    public_key = models.CharField(max_length=44, verbose_name='VPN Service pubkey', default=PRIVATE_KEY)
    private_key = models.CharField(max_length=44, verbose_name='VPN Service privkey', default=PUBLIC_KEY)
    server = models.ForeignKey(VPNServer, on_delete=models.CASCADE, verbose_name='VPN server')

    def __str__(self):
        return f'{self.service_name}'

    def get_absolute_url(self):
        return reverse('mainapp:vpn_service_details_page', kwargs={
            'pk': self.pk
        })


class VPNClient(models.Model):
    """VPN Client model"""
    client_name = models.CharField(max_length=255, verbose_name='VPN Client name')
    client_email = models.CharField(max_length=255, verbose_name='VPN Client email', validators=[validate_email])
    vpn_service = models.ForeignKey(VPNService, on_delete=models.CASCADE, verbose_name='VPN Service')

    def __str__(self):
        return f'{self.client_name}'


# TO DO
# 1. Replace keys generating logic to save method
class VPNDevice(models.Model):
    """VPN Device model"""
    PRIVATE_KEY, PUBLIC_KEY = generate_keys()
    DEVICE_TYPES = (
        ('pc', 'PC'),
        ('sm', 'Smartphone')
    )

    device_name = models.CharField(max_length=255, verbose_name='VPN Device name')
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, verbose_name='VPN Device type')
    private_ip = models.CharField(max_length=15, verbose_name='VPN Device ip', validators=[validate_ipv4_address])
    public_key = models.CharField(max_length=44, verbose_name='VPN Device pubkey', default=PUBLIC_KEY)
    private_key = models.CharField(max_length=44, verbose_name='VPN Device privkey', default=PRIVATE_KEY)
    client = models.ForeignKey(VPNClient, on_delete=models.CASCADE, verbose_name='VPN Client')

    def __str__(self):
        return f'{self.device_name}'
