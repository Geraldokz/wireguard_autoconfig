import smtplib
from email.message import EmailMessage
from typing import List

from config import EMAIL_USER, EMAIL_PASSWORD
from schemas import AccessEmailMessage


def send_emails(messages: List[AccessEmailMessage]) -> None:
    """Запускает рассылку писем по всем получателям"""
    with smtplib.SMTP_SSL('smtp.yandex.ru') as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)

        for message in messages:
            email_message = _create_email_message(message)
            smtp.send_message(email_message)
            print(f'access email to {message.email_to} send successfully!')


def _create_email_message(message: AccessEmailMessage) -> EmailMessage:
    """Создает письма типа EmailMessage"""
    email_message = EmailMessage()
    email_message['Subject'] = message.subject
    email_message['From'] = EMAIL_USER
    email_message['To'] = message.email_to
    email_message.set_content(message.body)
    _add_attachments_to_message(email_message, message.attachments)
    return email_message


def _add_attachments_to_message(message: EmailMessage, attachments: List[str]) -> None:
    """Добавляет вложения в письмо"""
    for attachment in attachments:
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_name = f.name.split('/')[-1]
        message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
