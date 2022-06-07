from os.path import exists
from typing import List

import yaml

from exceptions import ParsingException
from schemas import RawClientInfo, RawDeviceInfo


def parse_clients_file(file_path: str) -> List[RawClientInfo]:
    """Запускает парсинг файла c информацией о клиентах и их устройствах"""
    _validate_file(file_path)
    clients_info = _parse_yaml_file(file_path)
    clients = _get_clients_info(clients_info)
    return clients


def _validate_file(file_path: str) -> None:
    """Осуществляет проверку на существованиие файла и его расширение"""
    if not exists(file_path):
        raise ParsingException(f'file {file_path} does not exist')

    if not file_path.endswith('.yaml'):
        raise ParsingException(f'file {file_path} should be in yaml format')


def _parse_yaml_file(file_path: str) -> dict:
    """Парсит yaml и возвращает всю информацию в dict"""
    with open(file_path, 'r') as file:
        try:
            clients = yaml.safe_load(file)
        except yaml.YAMLError:
            raise ParsingException(f'error while loading yaml file {file_path}')
        return clients


def _get_clients_info(clients_info: dict) -> List[RawClientInfo]:
    """Преобразуем данные о клиентах в RawClientInfo и возвращаем их список"""
    clients = []
    for client in clients_info['clients']:
        try:
            devices_info = _get_devices_info(client['devices'])
            client_info = RawClientInfo(
                name=client['name'],
                email=client['email'],
                devices=devices_info
            )
        except TypeError:
            raise ParsingException('wrong client or device attribute name')
        clients.append(client_info)
    return clients


def _get_devices_info(devices_info: dict) -> List[RawDeviceInfo]:
    """Преобразует даные об устройствах в RawDeviceInfo и возвращает их список"""
    devices = [RawDeviceInfo(**device) for device in devices_info]
    return devices
