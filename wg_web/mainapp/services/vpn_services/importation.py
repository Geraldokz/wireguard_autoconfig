import json
from typing import NamedTuple, List

from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from mainapp.models import VPNService, VPNClient, VPNDevice, VPNServer
from mainapp.exceptions import VPNServiceImportError


class Device(NamedTuple):
    device_name: str
    device_type: str
    private_ip: str
    public_key: str
    private_key: str
    dns: str
    allowed_ips: str
    ka_check: int


class Client(NamedTuple):
    client_name: str
    client_email: str
    devices: List[dict]


class Service(NamedTuple):
    service_name: str
    vpn_network: str
    vpn_port: int
    private_ip: str
    vpn_if_name: str
    public_key: str
    private_key: str
    server: str
    clients: List[dict]


@transaction.atomic
def import_vpn_service(server_conf: bytes) -> None:
    """Create VPN Service with clients and devices"""
    json_config = json.loads(server_conf)

    try:
        service_config = Service(**json_config)
        server = _get_vpn_server(service_config.server)
        service = _create_service(service_config, server)
        _import_vpn_clients(service_config.clients, service)
    except ValidationError as errors:
        errors = dict(errors)
        validation_errors = ', '.join([errors[error][0].strip('.') for error in errors])
        raise VPNServiceImportError(f'Service validation error! Errors: {validation_errors}')
    except TypeError:
        raise VPNServiceImportError('Config names validation error!')
    except ValueError as err:
        raise VPNServiceImportError(err)


def _create_service(service_config: Service, server: VPNServer) -> VPNService:
    """Create VPN Service"""
    service = VPNService()
    service.service_name = service_config.service_name
    service.vpn_network = service_config.vpn_network
    service.vpn_port = service_config.vpn_port
    service.private_ip = service_config.private_ip
    service.vpn_if_name = service_config.vpn_if_name
    service.public_key = service_config.public_key
    service.private_key = service_config.private_key
    service.server = server

    service.full_clean()
    service.save()
    return service


def _get_vpn_server(server_name: str) -> VPNServer:
    """Find server id by hostname"""
    try:
        server = VPNServer.objects.get(hostname=server_name)
        return server
    except ObjectDoesNotExist:
        raise VPNServiceImportError(f'Server {server_name} does not exist!')


def _import_vpn_clients(clients_conf: List[dict], vpn_service: VPNService) -> None:
    """Import VPN Clients and Devices"""
    for client_conf in clients_conf:
        client = Client(**client_conf)
        vpn_client = _create_vpn_client(client, vpn_service)
        _import_vpn_devices(client.devices, vpn_client)


def _create_vpn_client(client: Client, vpn_service: VPNService) -> VPNClient:
    """Create VPN Client"""
    vpn_client = VPNClient()
    vpn_client.client_name = client.client_name
    vpn_client.client_email = client.client_email
    vpn_client.vpn_service = vpn_service

    vpn_client.full_clean()
    vpn_client.save()
    return vpn_client


def _import_vpn_devices(devices_conf: List[dict], vpn_client: VPNClient) -> None:
    """Import VPN Devices"""
    for device_conf in devices_conf:
        device = Device(**device_conf)
        _create_vpn_device(device, vpn_client)


def _create_vpn_device(device: Device, vpn_client: VPNClient) -> None:
    """Create VPN Device"""
    vpn_device = VPNDevice()
    vpn_device.device_name = device.device_name
    vpn_device.device_type = device.device_type
    vpn_device.private_ip = device.private_ip
    vpn_device.public_key = device.public_key
    vpn_device.private_key = device.private_key
    vpn_device.dns = device.dns
    vpn_device.allowed_ips = device.allowed_ips
    vpn_device.ka_check = device.ka_check
    vpn_device.client = vpn_client

    vpn_device.full_clean()
    vpn_device.save()
