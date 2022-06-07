import base64
from typing import List

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

from .parse_clients_file import RawClientInfo
from schemas import WireGuardKeys


def generate_clients_keys(clients_info: List[RawClientInfo]) -> List[WireGuardKeys]:
    """Проходится по списку всех клиентов и устройств и генерит пары ключей"""
    wireguard_keys = []
    for client in clients_info:
        for device in client.devices:
            device_keys = _generate_wireguard_keys()
            wireguard_keys.append(device_keys)
    return wireguard_keys


def generate_server_keys() -> WireGuardKeys:
    """Генерит одну пару ключей для сервера"""
    wireguard_keys = _generate_wireguard_keys()
    return wireguard_keys


def _generate_wireguard_keys() -> WireGuardKeys:
    """Генерит приватный и публичный ключ"""
    private_key = _generate_private_key()
    public_key = _generate_public_key(private_key)
    wireguard_keys = WireGuardKeys(private_key=private_key, public_key=public_key)
    return wireguard_keys


def _generate_private_key() -> str:
    """Генерит приватный ключ"""
    private_key = base64.b64encode(
            X25519PrivateKey.generate().private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            )
        ).decode()
    return private_key


def _generate_public_key(private_key: str) -> str:
    """Генерит публичный ключ"""
    public_key = base64.b64encode(
            X25519PrivateKey.from_private_bytes(base64.b64decode(private_key.encode()))
            .public_key()
            .public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ).decode()
    return public_key
