from ipaddress import IPv4Network
from typing import Type, List

from mainapp.exceptions import NetworkGeneratingException
from mainapp.services.vpn_services.service import get_all_vpn_service_devices, get_vpn_service
from mainapp.models import VPNDevice


def generate_vpn_device_ip(service_id: int) -> str:
    """Find free ip address for device"""
    vpn_service = get_vpn_service(service_id)
    vpn_devices = get_all_vpn_service_devices(service_id)
    busy_ips = _get_vpn_busy_ip(vpn_devices)
    free_ip = _find_free_ip(busy_ips, vpn_service.vpn_network)
    return free_ip


def _get_vpn_busy_ip(vpn_devices: List[Type[VPNDevice]]) -> List[str]:
    """Find service busy ip addresses"""
    busy_ips = [device.private_ip for device in vpn_devices]
    return busy_ips


def _find_free_ip(busy_ips: List[str], vpn_network: str) -> str:
    """Find free ip in VPN network"""
    vpn_network = IPv4Network(vpn_network)

    for ip in [*vpn_network][2:]:
        if str(ip) not in busy_ips:
            return str(ip)

    raise NetworkGeneratingException(f'no free ip in vpn service network')
