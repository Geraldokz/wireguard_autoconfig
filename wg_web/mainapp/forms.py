from django import forms

from .models import VPNServer, VPNService, VPNDevice, VPNClient


class VPNServerForm(forms.ModelForm):
    """Server creating/updating form"""
    class Meta:
        model = VPNServer
        fields = ['hostname', 'public_ip', 'if_name']
        widgets = {
            'hostname': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'public_ip': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'if_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }


class VPNServiceForm(forms.ModelForm):
    """VPN Service creating/updating form"""
    class Meta:
        model = VPNService
        fields = ['service_name', 'vpn_network', 'vpn_port', 'private_ip', 'vpn_if_name', 'server']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'vpn_network': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'net_mask': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'vpn_port': forms.NumberInput(attrs={'class': 'form-control mb-2'}),
            'vpn_if_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'private_ip': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'server': forms.Select(attrs={'class': 'form-control mb-3'}),
        }


class VPNClientForm(forms.ModelForm):
    """VPN Client creating/updating form"""
    class Meta:
        model = VPNClient
        fields = ['client_name', 'client_email', 'vpn_service']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'client_email': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'vpn_service': forms.Select(attrs={'class': 'form-control mb-3', 'readonly': 'readonly'}),
        }


class VPNDeviceForm(forms.ModelForm):
    """VPN Client creating/updating form"""
    class Meta:
        model = VPNDevice
        fields = [
            'device_name', 'device_type', 'private_ip', 'public_key',
            'private_key', 'dns', 'allowed_ips', 'ka_check', 'client'
        ]
        widgets = {
            'device_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'device_type': forms.Select(attrs={'class': 'form-select mb-2'}),
            'private_ip': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'public_key': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'private_key': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'dns': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'allowed_ips': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'ka_check': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'client': forms.Select(attrs={'class': 'form-control mb-3', 'readonly': 'readonly'}),
        }
