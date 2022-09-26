import json
import os

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIGURATION_FILE = 'config.json'

with open(os.path.join(FILE_PATH, CONFIGURATION_FILE)) as file:
    data = json.load(file)

BOT_TOKEN = data['BOT_TOKEN']

# mongo settings
DB_NAME = data['DB_NAME']
HOST_MONGO = data['MONGO_CONTAINER_IP']
DB_PORT = data['DB_PORT']


# webhook settings
WEBHOOK_HOST = data['DOMAIN_NAME_OR_IP']
WEBHOOK_PATH = '/tg'
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = data['APP_BOT_PORT']