from ipaddress import IPv4Network
from typing import List

from config import WIREGUARD_SUBNET
from exceptions import IPAddressGeneratorException

from .parse_clients_file import RawClientInfo

vpn_network = IPv4Network(WIREGUARD_SUBNET)


def create_clients_addresses(clients_info: List[RawClientInfo]) -> List[str]:
    """Выделяет адрессацию для устройств"""
    device_count = _count_devices(clients_info)
    clients_addresses = list(map(str, list(vpn_network)[2:device_count+2]))
    if device_count != len(clients_addresses):
        raise IPAddressGeneratorException(f'too many devices for network {vpn_network}')
    return clients_addresses


def create_sever_address() -> str:
    """Выделяет первый адрес из подсети для сервера"""
    server_address = list(vpn_network)[1]
    return str(server_address)


def _count_devices(clients_info: List[RawClientInfo]) -> int:
    """Считает количество устройств"""
    devices_count = 0
    for client in clients_info:
        for device in client.devices:
            devices_count += 1
    return devices_count


if __name__ == '__main__':
    for ip in list(vpn_network)[::500]:
        print(ip)