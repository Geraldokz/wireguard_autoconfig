from typing import NamedTuple

from services import parse_clients_file


class WireguardDefaultSetting(NamedTuple):
    project_name: str
    public_ip: str
    default_interface: str
    clients_file_path: str


def create_wireguard_config(wireguard_settings: WireguardDefaultSetting) -> None:
    """Запускает процесс создания конфигурации wireguard с нуля"""
    parse_clients_file(wireguard_settings.clients_file_path)


def update_wireguard_config(wireguard_setting: WireguardDefaultSetting) -> None:
    """Запускает процесс обновления конфигурации wireguard"""
    pass
