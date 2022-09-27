import os

from base import installer


DIR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = 'base'
PATH_TO_BASE_DIR = os.path.join(DIR_PATH, BASE_DIR)
DOMAIN_NAME_OR_IP = installer.check_host_ip()

# === config files
APP_CONFIG = 'config.json'
NGINX_CONFIG_TEMPLATENAME = 'nginx'
NGINX_CONFIG_FILENAME = 'nginx.conf'

# === bot configs
BOT_TOKEN = '1619380625:AAFqQC-Uzy7zOQ5SBw8QxZBbJRytp69ffgo'
DB_NAME = 'CURRENCY_BOT'
DB_PORT = '27017'
APP_BOT_PORT = 5000

# === docker-volume names
MONGO_DB_VOLUME_NAME = 'mongo_db'
MONGO_VOLUME_DIRECTORY_NAME = 'mongo_db'

# === api configs
APP_API_PORT = 8080

# === docker image names
APP_BOT_IMAGE_NAME = 'app_bot'
APP_API_IMAGE_NAME = 'app_api'
NGNIX_IMAGE_NAME = 'nginx'
MONGO_DB_IMAGE_NAME = 'mongo'

# === docker containers names/Dockerfiles projects folders
APP_BOT_CONTAINER_NAME = 'app_bot'
APP_API_CONTAINER_NAME = 'app_api'
NGNIX_CONTAINER_NAME = 'nginx'
MONGO_DB_CONTAINER_NAME = 'mongo'

# === Install docker ==
installer.install_from_execute_file(PATH_TO_BASE_DIR)

# === create certificate and key
installer.create_ssl_cert(DOMAIN_NAME_OR_IP, PATH_TO_BASE_DIR)
# === copy cert to bot-app key-directory
copy_path_from = os.path.join(PATH_TO_BASE_DIR,'keys/bot_cert.pem')
copy_path_to = os.path.join(DIR_PATH, 'app_bot/key')

installer.copy_file(copy_path_from, copy_path_to)

# === created docker-volume for mongo
installer.create_docker_volume(PATH_TO_BASE_DIR, MONGO_VOLUME_DIRECTORY_NAME, MONGO_DB_VOLUME_NAME)

# === run docker-image mongo-db
installer.run_docker_container(
    con_name=f'--name {MONGO_DB_CONTAINER_NAME}', 
    p=f'-p {DB_PORT}:{DB_PORT}', 
    img_name=MONGO_DB_IMAGE_NAME
    )

# === find out IP docker mongo-container
MONGO_CONTAINER_IP = installer.check_docker_container_ip(MONGO_DB_CONTAINER_NAME)

# === sind info mongodb (container ip, db_name, db_port), bot_tocken,  to config.json
config_data = {
        'BOT_TOKEN': BOT_TOKEN,
        'MONGO_CONTAINER_IP': MONGO_CONTAINER_IP,
        'DB_NAME': DB_NAME,
        'DB_PORT': DB_PORT,
        'DOMAIN_NAME_OR_IP': DOMAIN_NAME_OR_IP,
        'APP_BOT_PORT': APP_BOT_PORT,
        'APP_API_PORT': APP_API_PORT
    }
installer.sind_data_to_config_json(config_data, APP_CONFIG, PATH_TO_BASE_DIR)

# === create docker-image with app_api
path_to_dockerfile_app_bot = os.path.join(DIR_PATH, APP_BOT_IMAGE_NAME)
installer.create_docker_image(APP_BOT_IMAGE_NAME, path_to_dockerfile_app_bot)

# === run docker-container bot_app
block_p = f'-p {APP_BOT_PORT}:{APP_API_PORT}'
block_v = f'{os.path.join(DIR_PATH, os.path.join(BASE_DIR, APP_CONFIG))}:/usr/src/app/bot/{APP_CONFIG}'
installer.run_docker_container(APP_BOT_CONTAINER_NAME, p=block_p, v=block_v, img_name=APP_BOT_IMAGE_NAME)

# === create docker-image with api_app
path_to_dockerfile_app_api = os.path.join(DIR_PATH, APP_API_IMAGE_NAME)
installer.create_docker_image(APP_API_IMAGE_NAME, path_to_dockerfile_app_api)

# === run docker-container app_api
block_v = f'{os.path.join(PATH_TO_BASE_DIR, APP_CONFIG)}:/usr/src/app/{APP_CONFIG}'
block_p = f'-p {APP_API_PORT}:{APP_API_PORT}'
installer.run_docker_container(APP_API_CONTAINER_NAME, p=block_p, v=block_v, img_name=APP_API_IMAGE_NAME)

# === find out IP docker app_bot-container
APP_BOT_IP = installer.check_docker_container_ip(APP_BOT_CONTAINER_NAME)

# === find out IP docker app_api-container
APP_API_IP = installer.check_docker_container_ip(APP_API_CONTAINER_NAME)

# === create nginx configuration file
installer.create_file_nginx_config(
    PATH_TO_BASE_DIR, 
    NGINX_CONFIG_TEMPLATENAME, 
    NGINX_CONFIG_FILENAME, 
    APP_BOT_IP, APP_API_IP)

# === create docker-image wih nginx
path_to_dockerfile_nginx = os.path.join(PATH_TO_BASE_DIR, NGNIX_IMAGE_NAME)
installer.create_docker_image(APP_API_IMAGE_NAME, path_to_dockerfile_app_api)

# === run docker container with nginx
block_p = '-p 80:80 -p 443:443'
block_v = f'{os.path.join(PATH_TO_BASE_DIR, NGINX_CONFIG_FILENAME)}:/etc/nginx/conf.d/default.conf'
installer.run_docker_container(NGNIX_CONTAINER_NAME, p=block_p, v=block_v, img_name=NGNIX_IMAGE_NAME)