import json
from typing import NamedTuple, List, Type

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
    devices: List[Device]


class Service(NamedTuple):
    service_name: str
    vpn_network: str
    vpn_port: int
    private_ip: str
    vpn_if_name: str
    public_key: str
    private_key: str
    server: str
    clients: List[Client]


@transaction.atomic
def import_vpn_service(server_conf: bytes) -> None:
    """Create VPN Service with clients and devices"""
    json_config = json.loads(server_conf)

    service_config = Service(**json_config)
    server = _get_vpn_server(service_config.server)

    try:
        _create_service(service_config, server)
    except ValidationError as errors:
        errors = dict(errors)
        validation_errors = ', '.join([errors[error][0].strip('.') for error in errors])
        raise VPNServiceImportError(f'Service validation error! Errors: {validation_errors}')


def _create_service(service_config: Service, server: VPNServer) -> None:
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


def _get_vpn_server(server_name: str) -> VPNServer:
    """Find server id by hostname"""
    try:
        server = VPNServer.objects.get(hostname=server_name)
        return server
    except ObjectDoesNotExist:
        raise VPNServiceImportError(f'Server {server_name} does not exist!')
