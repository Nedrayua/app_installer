import os
import json

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIGURATION_FILE = 'config.json'

with open(os.path.join(FILE_PATH, CONFIGURATION_FILE)) as file:
    data = json.load(file)


class Configuration:
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


# mongo settings
DB_NAME = data['DB_NAME']
HOST_MONGO = data['MONGO_CONTAINER_IP']
DB_PORT = int(data['DB_PORT'])


# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(data['APP_API_PORT'])