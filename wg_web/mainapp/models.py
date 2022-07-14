from ipaddress import IPv4Network

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


# TO DO: add keys validation
class VPNService(models.Model):
    """VPN Service model"""
    service_name = models.CharField(max_length=255, verbose_name='VPN Service name')
    vpn_network = models.CharField(max_length=18, verbose_name='VPN Service network', validators=[validate_network])
    vpn_port = models.IntegerField(verbose_name='VPN port')
    private_ip = models.CharField(max_length=15, verbose_name='VPN Service ip', validators=[validate_ipv4_address])
    vpn_if_name = models.CharField(max_length=50, verbose_name='VPN Service interface name', default='wg0')
    public_key = models.CharField(max_length=44, verbose_name='VPN Service pubkey')
    private_key = models.CharField(max_length=44, verbose_name='VPN Service privkey')
    server = models.ForeignKey(VPNServer, on_delete=models.CASCADE, verbose_name='VPN server')

    def __str__(self):
        return f'{self.service_name}'

    def get_absolute_url(self):
        return reverse('mainapp:vpn_service_details_page', kwargs={
            'pk': self.pk
        })

    def save(self, *args, **kwargs):
        """Take first network ip for vpn service address"""
        self.private_ip = str(IPv4Network(self.vpn_network)[1])
        super().save(*args, **kwargs)


class VPNClient(models.Model):
    """VPN Client model"""
    client_name = models.CharField(max_length=255, verbose_name='VPN Client name')
    client_email = models.CharField(max_length=255, verbose_name='VPN Client email', validators=[validate_email])
    vpn_service = models.ForeignKey(VPNService, on_delete=models.CASCADE, verbose_name='VPN Service')

    def __str__(self):
        return f'{self.client_name}'


# TO DO: add extra validation to ip and keys
class VPNDevice(models.Model):
    """VPN Device model"""
    DEVICE_TYPES = (
        ('pc', 'PC'),
        ('sm', 'Smartphone')
    )

    device_name = models.CharField(max_length=255, verbose_name='VPN Device name')
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, verbose_name='VPN Device type')
    private_ip = models.CharField(max_length=15, verbose_name='VPN Device ip', validators=[validate_ipv4_address])
    public_key = models.CharField(max_length=44, verbose_name='VPN Device pubkey')
    private_key = models.CharField(max_length=44, verbose_name='VPN Device privkey')
    dns = models.CharField(max_length=15, verbose_name='DNS ip', default='8.8.8.8', validators=[validate_ipv4_address])
    allowed_ips = models.CharField(max_length=255, verbose_name='Allowed ips', default='0.0.0.0/0')
    ka_check = models.IntegerField(verbose_name='Keepalive check interval', default=20)
    client = models.ForeignKey(VPNClient, on_delete=models.CASCADE, verbose_name='VPN Client')

    def __str__(self):
        return f'{self.device_name}'
