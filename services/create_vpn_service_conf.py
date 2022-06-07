from typing import List

from config import WIREGUARD_NETWORK, WIREGUARD_PORT
from schemas import (
    RawClientInfo,
    RawDeviceInfo,
    FullClientInfo,
    FullDeviceInfo,
    WireGuardKeys,
    WireguardDefaultSettings,
    VPNServiceInfo
)


def create_vpn_service_conf(wireguard_default: WireguardDefaultSettings, clients_info: List[RawClientInfo],
                            devices_keys: List[WireGuardKeys], server_keys: WireGuardKeys,
                            devices_vpn_ip: List[str], server_vpn_ip: str) -> VPNServiceInfo:
    """Собирает полную информацию о развертываемом сервисе в структуру VPNServer"""
    clients = _create_full_clients_info(clients_info, devices_keys, devices_vpn_ip)
    vpn_server = VPNServiceInfo(
        name=wireguard_default.name,
        network=WIREGUARD_NETWORK,
        port=WIREGUARD_PORT,
        vpn_ip=server_vpn_ip,
        public_ip=wireguard_default.public_ip,
        interface=wireguard_default.interface,
        private_key=server_keys.private_key,
        public_key=server_keys.public_key,
        clients=clients
    )
    return vpn_server


def _create_full_clients_info(clients_info: List[RawClientInfo],
                              devices_keys: List[WireGuardKeys], devices_vpn_ip: List[str]) -> List[FullClientInfo]:
    """Собирает полную информацию о клиентах в структуру ClientInfo и возвращает их список"""
    full_clients_info = []
    for raw_client in clients_info:
        devices = _create_full_devices_info(raw_client.devices, devices_keys, devices_vpn_ip)
        client = FullClientInfo(
            name=raw_client.name,
            email=raw_client.email,
            devices=devices
        )
        full_clients_info.append(client)
    return full_clients_info


def _create_full_devices_info(devices_info: List[RawDeviceInfo], devices_keys: List[WireGuardKeys],
                              devices_vpn_ip: List[str]) -> List[FullDeviceInfo]:
    """Собирает полную информацию об устройствах в структуру DeviceInfo и возвращает их список"""
    devices = []
    for raw_device in devices_info:
        vpn_ip = _cut_ip_from_list(devices_vpn_ip)
        wireguard_keys = _cut_keys_from_list(devices_keys)
        private_key = wireguard_keys.private_key
        public_key = wireguard_keys.public_key
        device_info = FullDeviceInfo(
            name=raw_device.name,
            vpn_ip=vpn_ip,
            private_key=private_key,
            public_key=public_key,
            type=raw_device.type
        )
        devices.append(device_info)
    return devices


def _cut_ip_from_list(devices_vpn_ip: List[str]) -> str:
    """Возвращает ip из списка по 0 индексу и удаляет его из списка"""
    vpn_ip = devices_vpn_ip[0]
    devices_vpn_ip.pop(0)
    return vpn_ip


def _cut_keys_from_list(devices_keys: List[WireGuardKeys]) -> WireGuardKeys:
    """Возвращает пару wireguard ключей по 0 индексу и удаляет их из списка"""
    wireguard_keys = devices_keys[0]
    devices_keys.pop(0)
    return wireguard_keys
