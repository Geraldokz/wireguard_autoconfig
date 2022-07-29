import json
from typing import NamedTuple

from django.core.exceptions import ValidationError

from mainapp.models import VPNServer
from mainapp.exceptions import VPNServerImportError


class Server(NamedTuple):
    hostname: str
    public_ip: str
    if_name: str


def import_vpn_server(server_conf: bytes) -> None:
    """Create server from json config"""
    config = json.loads(server_conf)
    try:
        server_fields = Server(**config)
        _create_vpn_server(server_fields)
    except ValueError as err:
        raise VPNServerImportError(err)
    except TypeError:
        raise VPNServerImportError('Config names validation error!')
    except ValidationError as errors:
        errors = dict(errors)
        validation_errors = ', '.join([errors[error][0].strip('.') for error in errors])
        raise VPNServerImportError(f'Model validation error! Errors: {validation_errors}')


def _create_vpn_server(server_conf: Server) -> None:
    """Create VPN Server"""
    server = VPNServer()
    server.hostname = server_conf.hostname
    server.public_ip = server_conf.public_ip
    server.if_name = server_conf.if_name

    server.full_clean()
    server.save()
