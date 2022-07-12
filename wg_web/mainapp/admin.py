from django.contrib import admin

from .models import VPNServer, VPNService, VPNClient, VPNDevice


@admin.register(VPNServer)
class VPNServerAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'public_ip', 'if_name')


@admin.register(VPNService)
class VPNServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'vpn_network', 'vpn_port', 'private_ip', 'get_server_name', 'get_server_ip')

    @admin.display(ordering='server_name', description='Server hostname')
    def get_server_name(self, obj):
        return obj.server.hostname

    @admin.display(ordering='server_ip', description='Server IP')
    def get_server_ip(self, obj):
        return obj.server.public_ip


@admin.register(VPNClient)
class VPNClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'get_vpn_service_name')

    @admin.display(ordering='client_name', description='VPN Service name')
    def get_vpn_service_name(self, obj):
        return obj.vpn_service.service_name


@admin.register(VPNDevice)
class VPNDeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'private_ip', 'get_client_name')

    @admin.display(ordering='client_name', description='Client name')
    def get_client_name(self, obj):
        return obj.client.client_name
