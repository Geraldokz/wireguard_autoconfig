import os

from dotenv import load_dotenv

load_dotenv()

WORK_DIR = os.environ.get('WORK_DIR')
WIREGUARD_NETWORK = os.environ.get('WIREGUARD_NETWORK')
WIREGUARD_PORT = os.environ.get('WIREGUARD_PORT')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
