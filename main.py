import argparse

from schemas import WireguardDefaultSettings
from script_methods import create_wireguard_config, update_wireguard_config


script_parser = argparse.ArgumentParser()
script_parser.add_argument('method', choices=['create', 'update'], help='Choose script method')
script_parser.add_argument('-p', '--project', required=True, metavar='', help='VPN project name')
script_parser.add_argument('-a', '--address', required=True, metavar='', help='VPN server public ip')
script_parser.add_argument('-i', '--interface', required=True, metavar='', help='VPN server default interface name')
script_parser.add_argument('-f', '--file', required=True, metavar='', help='VPN clients file path')
script_args = script_parser.parse_args()


if __name__ == '__main__':
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
