from typing import List, Type

from django.core.exceptions import ObjectDoesNotExist

from mainapp.exceptions import VPNServiceException
from mainapp.models import VPNService, VPNClient, VPNDevice


def get_vpn_service(service_id: int) -> Type[VPNService]:
    """Get VPN Service by id"""
    try:
        vpn_service = VPNService.objects.get(pk=service_id)
        return vpn_service
    except ObjectDoesNotExist:
        raise VPNServiceException(f'vpn service with {service_id} id does not exist')


def get_vpn_service_clients(vpn_service_id: int) -> List[Type[VPNClient]]:
    """Get all VPN Service clients by service id"""
    vpn_clients = VPNClient.objects.filter(vpn_service=vpn_service_id)
    return vpn_clients


def get_all_vpn_service_devices(vpn_service_id: int) -> List[Type[VPNDevice]]:
    """Get all VPN Service devices by service id"""
    vpn_devices = []
    vpn_clients = get_vpn_service_clients(vpn_service_id)

    for client in vpn_clients:
        devices = VPNDevice.objects.filter(client=client.pk)
        for device in devices:
            vpn_devices.append(device)

    return vpn_devices
