SUCCESS = f'{"=" * 50}SUCCESS!{"=" * 50}'
ERROR = f'{"=" * 50}ERROR!{"=" * 50}'

CON = 'container'
IMG = 'image'
VOL = 'volume'

COM_CHECK = {
    'container': 'sudo docker ps -a',
    'image': 'sudo docker images -a',
    'volume': 'sudo docker volume ls'
}

COM_RM = {
    'container': 'sudo docker rm --force {}',
    'image': 'sudo docker rmi --force {}',
    'volume': 'sudo docker volume rm --force {}'
}

NAMES = {
    'container': 'NAMES',
    'image': 'REPOSITORY',
    'volume': 'VOLUME NAME'
}

IDENT = {
    'container': 'CONTAINER ID',
    'image': 'IMAGE ID',
    'volume': 'VOLUME NAME'
}

MESSAGES = {
    'container': 'Docker have containers in repository: {}',
    'image': 'Docker have images in repository: {}',
    'volume': 'Docker have volumes in repository: {}'
}

COM_CERT_CREATE = 'openssl req -newkey rsa:2048 -sha256 -nodes -keyout {0}/keys/cert_pkey.key \
            -x509 -days 365 -out {0}/keys/bot_cert.pem -subj "/C=UA/ST=Kyev/L=None/O=None/CN={1}"'

COM_DOK_VOLUME_CREATE = 'sudo docker volume create {} -o device={} -o type=none -o o=bind'

COM_DOK_VOLUME_CREATE

COM_DOK_VOLUME_CREATE