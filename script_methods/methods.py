from config import WORK_DIR
from schemas import WireguardDefaultSettings
from services import (
    parse_clients_file,
    create_folder,
    generate_clients_keys,
    generate_server_keys,
    create_clients_addresses,
    create_sever_address,
    create_vpn_service_conf,
    create_wg_configs
)


def create_wireguard_config(wireguard_settings: WireguardDefaultSettings) -> None:
    """Запускает процесс создания конфигурации wireguard с нуля"""
    create_folder(f'{WORK_DIR}/{wireguard_settings.name}')
    clients_info = parse_clients_file(wireguard_settings.clients_file_path)
    devices_wireguard_keys = generate_clients_keys(clients_info)
    server_wireguard_keys = generate_server_keys()
    devices_vpn_ip = create_clients_addresses(clients_info)
    server_vpn_ip = create_sever_address()
    vpn_service = create_vpn_service_conf(wireguard_settings, clients_info, devices_wireguard_keys,
                                          server_wireguard_keys, devices_vpn_ip, server_vpn_ip)
    create_wg_configs(vpn_service)


def update_wireguard_config(wireguard_setting: WireguardDefaultSettings) -> None:
    """Запускает процесс обновления конфигурации wireguard"""
    pass
