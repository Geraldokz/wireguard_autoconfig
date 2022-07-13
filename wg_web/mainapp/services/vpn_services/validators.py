from ipaddress import IPv4Network, AddressValueError

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_network(network: str) -> None:
    """Validate network"""
    allowed_net_mask = ('8', '16', '24')

    try:
        IPv4Network(network)
    except (AddressValueError, ValueError):
        raise ValidationError(
            gettext_lazy(f'{network} is not valid ipv4 network.')
        )

    try:
        net, mask = network.split('/')
    except ValueError:
        raise ValidationError(
            gettext_lazy('Netmask not specified.')
        )

    if mask not in allowed_net_mask:
        raise ValidationError(
            gettext_lazy(f'Net mask /{mask} not allowed. Choose 8, 16 or 24')
        )
