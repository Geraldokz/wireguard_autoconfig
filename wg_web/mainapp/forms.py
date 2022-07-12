from django import forms

from .models import VPNServer, VPNService, VPNDevice, VPNClient


class VPNServerForm(forms.ModelForm):
    """Server creating form"""
    class Meta:
        model = VPNServer
        fields = ['hostname', 'public_ip', 'if_name']
        widgets = {
            'hostname': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'public_ip': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'if_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }
