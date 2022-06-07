import os

from dotenv import load_dotenv

load_dotenv()

WORK_DIR = os.environ.get('WORK_DIR')
WIREGUARD_SUBNET = os.environ.get('WIREGUARD_SUBNET')
WIREGUARD_PORT = os.environ.get('WIREGUARD_PORT')
