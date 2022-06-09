import argparse

from schemas import WireguardDefaultSettings, MailingInfo
from script_methods import create_wireguard_config, update_wireguard_config, send_access_emails


script_parser = argparse.ArgumentParser()
script_parser.add_argument('method', choices=['create', 'update', 'mail'], help='Choose script method')
script_parser.add_argument('-p', '--project', metavar='', help='VPN project name')
script_parser.add_argument('-a', '--address', metavar='', help='VPN server public ip')
script_parser.add_argument('-i', '--interface', metavar='', help='VPN server default interface name')
script_parser.add_argument('-f', '--file', metavar='', help='VPN clients file path')

script_parser.add_argument('-c', '--client', metavar='', help='Clients to send mail')
script_parser.add_argument('-s', '--subject', metavar='', help='Letter subject')
script_parser.add_argument('-t', '--text', metavar='', help='Letter text')
script_parser.add_argument('-g', '--guide', metavar='', help='VPN Instruction Guide')

script_args = script_parser.parse_args()


if __name__ == '__main__':
    if script_args.method in ('create', 'update'):
        wireguard_settings = WireguardDefaultSettings(
            name=script_args.project,
            public_ip=script_args.address,
            interface=script_args.interface,
            clients_file_path=script_args.file
        )
        if script_args.method == 'create':
            create_wireguard_config(wireguard_settings)
        elif script_args.method == 'update':
            update_wireguard_config(wireguard_settings)
    elif script_args.method == 'mail':
        mailing_info = MailingInfo(
            vpn_project=script_args.project,
            vpn_client=script_args.client,
            instruction_path=script_args.guide,
            subject=script_args.subject,
            mail_text=script_args.text
        )
        send_access_emails(mailing_info)
