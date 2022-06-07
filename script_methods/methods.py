from typing import NamedTuple

from services import (
    parse_clients_file,
    create_project_folder,
    generate_clients_keys,
    generate_server_keys,
    create_clients_addresses,
    create_sever_address,
    create_vpn_service_conf
)


class WireguardDefaultSetting(NamedTuple):
    project_name: str
    public_ip: str
    default_interface: str
    clients_file_path: str


def create_wireguard_config(wireguard_settings: WireguardDefaultSetting) -> None:
    """Запускает процесс создания конфигурации wireguard с нуля"""
    create_project_folder(wireguard_settings.project_name)
    clients_info = parse_clients_file(wireguard_settings.clients_file_path)
    devices_wireguard_keys = generate_clients_keys(clients_info)
    server_wireguard_keys = generate_server_keys()
    devices_vpn_ip = create_clients_addresses(clients_info)
    server_vpn_ip = create_sever_address()
    vpn_server = create_vpn_service_conf(wireguard_settings, clients_info, devices_wireguard_keys,
                                         server_wireguard_keys, devices_vpn_ip, server_vpn_ip)


def update_wireguard_config(wireguard_setting: WireguardDefaultSetting) -> None:
    """Запускает процесс обновления конфигурации wireguard"""
    pass
