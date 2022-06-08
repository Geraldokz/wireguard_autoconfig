import qrcode

from config import WORK_DIR
from exceptions import ConfigCreatorException
from schemas import VPNServiceInfo, FullDeviceInfo
from .manage_project_folder import create_folder


def create_wg_configs(vpn_service: VPNServiceInfo) -> None:
    """Создает конфиги конфиги сервера и клиентов"""
    _create_server_wg_config(vpn_service)
    _create_clients_configs(vpn_service)


def _create_server_wg_config(vpn_service: VPNServiceInfo) -> None:
    """Создает конфиг для сервера"""
    interface_record = _create_server_interface_record(vpn_service)
    peers_record = _create_server_peer_records(vpn_service)
    server_config = '\n\n'.join((interface_record, peers_record))
    _save_wg_config_file(f'{WORK_DIR}/{vpn_service.name}/wg0.conf', server_config)


def _create_server_interface_record(vpn_service: VPNServiceInfo) -> str:
    """Создает запись Interface в кофиге wireguard сервера"""
    address = vpn_service.vpn_ip + '/' + vpn_service.network.partition('/')[2]
    header_record = '[Interface]'
    address_record = f'Address = {address}'
    post_up_record = f'PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING' \
                     f' -o {vpn_service.interface} -j MASQUERADE'
    post_down_record = f'PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING' \
                       f' -o {vpn_service.interface} -j MASQUERADE'
    port_record = f'ListenPort = {vpn_service.port}'
    private_key_record = f'PrivateKey = {vpn_service.private_key}'
    interface_record = '\n'.join(
        (header_record, address_record, post_up_record, post_down_record, port_record, private_key_record)
    )
    return interface_record


def _create_server_peer_records(vpn_service: VPNServiceInfo) -> str:
    """Создает записи Peer в кофиге wireguard сервера"""
    peers = []
    for client in vpn_service.clients:
        create_folder(f'{WORK_DIR}/{vpn_service.name}/{client.name}')
        for device in client.devices:
            header_record = f'#Client: {client.name}, device: {device.name}, type: {device.type}\n[Peer]'
            public_key_record = f'PublicKey = {device.public_key}'
            address_record = f'AllowedIPs = {device.vpn_ip + "/32"}'
            peer_record = '\n'.join((header_record, public_key_record, address_record))
            peers.append(peer_record)
    full_peer_record = '\n\n'.join(peers)
    return full_peer_record


def _create_clients_configs(vpn_service: VPNServiceInfo) -> None:
    """Создает конфиг для устройств клиента"""
    for client in vpn_service.clients:
        for device in client.devices:
            interface_record = _create_device_interface_record(device)
            peer_record = _create_device_peer_record(vpn_service)
            device_config = '\n\n'.join((interface_record, peer_record))
            client_folder = f'{WORK_DIR}/{vpn_service.name}/{client.name}/'

            if device.type == 'smartphone':
                qrcode.make(device_config).save(f'{client_folder}/{device.name}_qr.png')
            elif device.type == 'pc':
                _save_wg_config_file(f'{client_folder}/{device.name}_wg.conf', device_config)
            else:
                raise ConfigCreatorException(
                    f'client {client.name} device {device.name} has wrong type {device.type}'
                )


def _create_device_interface_record(device: FullDeviceInfo) -> str:
    """Создает запись Interface в кофиге wireguard устройства"""
    header_record = '[Interface]'
    private_key_record = f'PrivateKey = {device.private_key}'
    address_record = f'Address = {device.vpn_ip + "/32"}'
    dns_record = f'DNS = 8.8.8.8'
    interface_record = '\n'.join((header_record, private_key_record, address_record, dns_record))
    return interface_record


def _create_device_peer_record(vpn_service: VPNServiceInfo) -> str:
    """Создает записи Peer в кофиге wireguard устройства"""
    header_record = '[Peer]'
    public_key_record = f'PublicKey = {vpn_service.public_key}'
    endpoint_record = f'Endpoint = {vpn_service.public_ip}:{vpn_service.port}'
    allowed_ip_record = f'AllowedIPs = 0.0.0.0/0'
    keep_alive_check_record = f'PersistentKeepalive = 20'
    peer_record = '\n'.join(
        (header_record, public_key_record, endpoint_record, allowed_ip_record, keep_alive_check_record)
    )
    return peer_record


def _save_wg_config_file(file_path: str, text: str) -> None:
    """Сохраняет файл с конфигом в нужной папке"""
    with open(file_path, 'w') as file:
        file.writelines(text)
