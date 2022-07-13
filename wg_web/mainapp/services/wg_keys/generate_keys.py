import base64
from typing import Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey


def generate_keys() -> Tuple[str, str]:
    """Generate wireguard key pair"""
    private_key = _generate_private_key()
    public_key = _generate_public_key(private_key)
    return private_key, public_key


def _generate_private_key() -> str:
    """Generate private key"""
    private_key = base64.b64encode(
            X25519PrivateKey.generate().private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            )
        ).decode()
    return private_key


def _generate_public_key(private_key: str) -> str:
    """Generate public key"""
    public_key = base64.b64encode(
            X25519PrivateKey.from_private_bytes(base64.b64decode(private_key.encode()))
            .public_key()
            .public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
        ).decode()
    return public_key
