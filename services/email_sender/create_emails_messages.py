import os
import json
from typing import List

from config import WORK_DIR
from exceptions import EmailSenderException
from schemas import AccessEmailMessage, MailingInfo, VPNServiceInfo, FullClientInfo


def create_emails_messages(mailing_info: MailingInfo) -> List[AccessEmailMessage]:
    """Создает список писем на отправку"""
    vpn_service_info = _get_vpn_service_info(mailing_info.vpn_project)

    if mailing_info.vpn_client:
        clients_name = mailing_info.vpn_client.split(';')
        clients_info = _find_clients_info(clients_name, vpn_service_info.clients)
    else:
        clients_info = vpn_service_info.clients

    email_messages = [_create_client_email_message(client, mailing_info) for client in clients_info]
    return email_messages


def _get_vpn_service_info(vpn_project: str) -> VPNServiceInfo:
    """Ищет json конфиг vpn сервиса и преобразует его в VPNServiceInfo"""
    json_config = f'{WORK_DIR}/{vpn_project}/{vpn_project}_vpn_config.json'
    try:
        with open(json_config) as f:
            vpn_service_info = VPNServiceInfo(**json.load(f))
            return vpn_service_info
    except FileNotFoundError:
        raise EmailSenderException(f'file {json_config} not found')


def _find_clients_info(clients_name: List[str], clients: List[FullClientInfo]) -> List[FullClientInfo]:
    """Находит информацию о клиентах"""
    clients_info = []
    for client in clients:
        if client.name in clients_name:
            clients_info.append(client)

    if not clients_info:
        raise EmailSenderException(f'clients {clients_name} not found')

    return clients_info


def _create_client_email_message(client_info: FullClientInfo, mailing_info: MailingInfo) -> AccessEmailMessage:
    """Создает объект типа AccessEmailMessage по данным о клиенте"""
    email_message = AccessEmailMessage(
        email_to=client_info.email,
        subject=mailing_info.subject,
        body=mailing_info.mail_text,
        attachments=_create_client_attachment(mailing_info, client_info.name)
    )
    return email_message


def _create_client_attachment(mailing_info: MailingInfo, client_name: str) -> List[str]:
    """Находит полные пути файлов для вложения"""
    attachments = []
    _add_vpn_guide_path(mailing_info.instruction_path, attachments)
    _add_wg_configs_path(f'{WORK_DIR}/{mailing_info.vpn_project}/{client_name}', attachments)
    return attachments


def _add_vpn_guide_path(guide_path: str, attachments: list) -> None:
    """Проверяет на существование файла с инструкцией и добавляет его в список вложений"""
    if os.path.exists(guide_path):
        attachments.append(guide_path)
    else:
        raise EmailSenderException(f'guide file {guide_path} does not exist')


def _add_wg_configs_path(client_folder: str, attachments: list) -> None:
    """Находит все файлы в директории клиента и добавляет их в список вложений"""
    try:
        configs = os.listdir(client_folder)
    except FileNotFoundError:
        raise EmailSenderException(f'client folder {client_folder} does not exist')

    for config in configs:
        attachments.append(f'{client_folder}/{config}')
