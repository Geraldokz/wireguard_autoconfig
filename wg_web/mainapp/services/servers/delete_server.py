from django.core.exceptions import ObjectDoesNotExist

from mainapp.exceptions import ServerDeleteException
from mainapp.models import VPNServer


def delete_vpn_server(server_id: int) -> None:
    """Delete VPN server object by id"""
    vpn_server = _get_vpn_server(server_id)
    vpn_server.delete()


def _get_vpn_server(server_id: int) -> VPNServer.objects:
    """Find VPN Server object by id"""
    try:
        vpn_server = VPNServer.objects.get(pk=server_id)
    except ObjectDoesNotExist:
        raise ServerDeleteException(f'vpn server with id {server_id} does not exist')
    return vpn_server
