import json

from schemas import VPNServiceInfo


def save_vpn_service_config_as_json(vpn_service_info: VPNServiceInfo, folder: str) -> None:
    """Сохраняем конфиг всего сервиса в json"""
    with open(f'{folder}/{vpn_service_info.name}_vpn_config.json', 'w') as file:
        json_config = json.dumps(vpn_service_info.dict(), indent=3)
        file.writelines(json_config)
