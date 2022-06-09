from typing import List, Literal, Optional

from pydantic import BaseModel


class WireguardDefaultSettings(BaseModel):
    name: str
    public_ip: str
    interface: str
    clients_file_path: str


class RawDeviceInfo(BaseModel):
    name: str
    type: Literal['smartphone', 'pc']


class RawClientInfo(BaseModel):
    name: str
    email: str
    devices: List[RawDeviceInfo]


class FullDeviceInfo(RawDeviceInfo):
    vpn_ip: str
    private_key: str
    public_key: str


class FullClientInfo(RawClientInfo):
    devices: List[FullDeviceInfo]


class VPNServiceInfo(BaseModel):
    name: str
    network: str
    port: int
    vpn_ip: str
    public_ip: str
    interface: str
    private_key: str
    public_key: str
    clients: List[FullClientInfo]


class WireGuardKeys(BaseModel):
    private_key: str
    public_key: str


class MailingInfo(BaseModel):
    vpn_project: str
    vpn_client: Optional[str]
    instruction_path: str
    subject: str
    mail_text: str


class AccessEmailMessage(BaseModel):
    email_to: str
    subject: str
    body: str
    attachments: List[str]
