from django.db import models


class VPNServer(models.Model):
    """VPN Server model"""
    hostname = models.CharField(max_length=255, verbose_name='Hostname')
    public_ip = models.CharField(max_length=15, verbose_name='Server IP')
    if_name = models.CharField(max_length=50, verbose_name='Eth interface name')

    def __str__(self):
        return f'{self.hostname}'


class VPNService(models.Model):
    """VPN Service model"""
    service_name = models.CharField(max_length=255, verbose_name='VPN Service name')
    vpn_network = models.CharField(max_length=18, verbose_name='VPN Service network')
    vpn_port = models.IntegerField(verbose_name='VPN port')
    private_ip = models.CharField(max_length=15, verbose_name='VPN Service ip')
    vpn_if_name = models.CharField(max_length=50, verbose_name='VPN Service interface name', default='eth0')
    public_key = models.CharField(max_length=44, verbose_name='VPN Service pubkey')
    private_key = models.CharField(max_length=44, verbose_name='VPN Service privkey')
    server = models.ForeignKey(VPNServer, on_delete=models.CASCADE, verbose_name='VPN server')

    def __str__(self):
        return f'{self.service_name}'


class VPNClient(models.Model):
    """VPN Client model"""
    client_name = models.CharField(max_length=255, verbose_name='VPN Client name')
    client_email = models.CharField(max_length=255, verbose_name='VPN Client email')
    vpn_service = models.ForeignKey(VPNService, on_delete=models.CASCADE, verbose_name='VPN Service')

    def __str__(self):
        return f'{self.client_name}'


class VPNDevice(models.Model):
    """VPN Device model"""
    DEVICE_TYPES = (
        ('pc', 'PC'),
        ('sm', 'Smartphone')
    )

    device_name = models.CharField(max_length=255, verbose_name='VPN Device name')
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, verbose_name='VPN Device type')
    private_ip = models.CharField(max_length=15, verbose_name='VPN Device ip')
    public_key = models.CharField(max_length=44, verbose_name='VPN Device pubkey')
    private_key = models.CharField(max_length=44, verbose_name='VPN Device privkey')
    client = models.ForeignKey(VPNClient, on_delete=models.CASCADE, verbose_name='VPN Client')

    def __str__(self):
        return f'{self.device_name}'
