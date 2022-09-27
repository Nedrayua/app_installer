
import subprocess as sub
import os
import json
from io import UnsupportedOperation
import time
import functools


# === docker ommands
COMM_CHECK_CONTAINERS = 'sudo docker ps -a'
COMM_CHECK_VOLUMES = 'sudo docker volme ls'
COMM_CHECK_IMAGES = 'sudo docker images -a'

def wait_for(seconds):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(seconds)
            return result
        return inner
    return decorator


@wait_for(2)
def check_host_ip():
    """
    Check IP of host
    """
    ip = sub.check_output('curl ifconfig.me', shell=True).decode()
    print(f'Host ip: {ip}')
    time.sleep(1)
    return ip


@wait_for(2)
def install_from_execute_file(path_to_resource:str=None) -> None:
    """
    :path_to_resource: resorce with executer files  
    Installation of dependencies necessary for correct operation on the
    host machine. Executes a list of instructions from .txt files located 
    in the directory specified in the argument
    """
    path_to_resource = path_to_resource or ''
    files = os.listdir(path_to_resource)
    executer_files = [f for f in files if f.startswith('execute_')]
    
    for filename in executer_files:
        with open(os.path.join(path_to_resource, filename), 'r') as file:
            install_result = []
            message_text = "{}{}. Return code: {}"
            marker = '.' * 100

            for line in file.readlines():
                line = line.replace('\n', '')
                result = sub.run(line, shell=True)
                install_result.append(result)
                statuscode = result.returncode
                message_status = 'Success' if statuscode == 0 else 'Fail'
                print(message_text.format(marker, message_status, statuscode))
            for result in install_result:
                print(result)


@wait_for(2)
def create_ssl_cert(domain_name, path_to_resource:str=None) -> None:
    """
    :domain_name: ip-address or domain name of host
    :path_entry_point: path to file execute program
    :path_to_resoure: path to foldere were executer file stored
    Creating certificate with key with put them in keys directory
    """
    cert_shell = 'openssl req -newkey rsa:2048 -sha256 -nodes -keyout {0}/keys/cert_pkey.key \
            -x509 -days 365 -out {0}/keys/bot_cert.pem -subj "/C=UA/ST=Kyev/L=None/O=None/CN={1}"'
    if not os.path.exists(os.path.join(path_to_resource, 'keys')):
        os.mkdir(os.path.join(path_to_resource, 'keys'))
    cert_command = sub.run(cert_shell.format(path_to_resource, domain_name), shell=True)
    if cert_command.returncode == 0:
        print('Successful create certificate with key for domainname: ', domain_name)
    else:
        print('Fail', cert_command, sep='\n')


@wait_for(2)
def parse_docker_check_result(command:str) -> list:
    """
    :command: - docker command for take a list of items
    for example: 'sudo docker ps'
    """
    data_str = sub.check_output(command, shell=True).decode()
    split_data_str = data_str.split('\n')
    list_data = [row.split('   ')for row in split_data_str]
    clean_data = map(lambda list_: [item.strip() for item in list_ if item], list_data)
    list_lists = [list(map_item) for map_item in clean_data if map_item]
    dict_data = []
    for list_ in list_lists[1:]:
       dict_data.append({k:w for (k, w) in zip(list_lists[0], list_)})
    return dict_data


@wait_for(2)
def create_docker_volume(path_to_resource:str, mongo_db_folder:str, docker_volume_name:str):
    """
    Create docker-volume with binding to folder
    """
    docker_command = 'sudo docker volume create {} -o device={} -o type=none -o o=bind'
    mongo_db_folder_path = os.path.join(path_to_resource, mongo_db_folder)
    if not os.path.exists(os.path.join(path_to_resource, mongo_db_folder)):
        os.mkdir(mongo_db_folder_path)
    aval_vilumes = [volume['VOLUME NAME'] for volume in parse_docker_check_result(COMM_CHECK_VOLUMES)]
    if docker_volume_name not in aval_vilumes:
        volume = sub.check_output(docker_command.format(docker_volume_name, mongo_db_folder_path), shell=True)
        print(f'Docker volume {docker_volume_name} created')
        return volume
    else:
        print(f'Docker volume {docker_volume_name} allready exist')


@wait_for(2)
def create_docker_image( image_name:str, path_to_dokerfile:str):
    """
    Created docker image
    """
    create_image_command = f'sudo docker build -t {image_name} {path_to_dokerfile}'
    aval_images = [image['REPOSITORY'] for image in parse_docker_check_result(COMM_CHECK_IMAGES)]
    if image_name not in aval_images:
        try:
            sub.check_output(create_image_command, shell=True)
            print(f'{"=" * 50}SUCCESS!{"=" * 50}\nDocker image: {image_name} successful created')
        except sub.CalledProcessError as ex:
            print(f'{"=" * 50}ERROR!{"=" * 50}\nSomething do wrong:', ex)
    else:
        print(f'Docker-image with name {image_name} already exist')
        

@wait_for(2)
def run_docker_container(con_name:str=None, p:str=None, v:str=None, *, img_name:str) -> None:
    con_name = con_name or ''
    p = p or ''
    v = v or ''
    docker_command = 'sudo docker run -d {con_name} {p} {v} {img_name}'
    avaliable_containers = [con['NAMES'] for con in parse_docker_check_result(COMM_CHECK_CONTAINERS)]
    if con_name not in avaliable_containers:
        try:
            sub.run(docker_command.format(con_name=con_name, p=p, v=v, img_name=img_name), shell=True)
            print(f'{"=" * 50}SUCCESS!{"=" * 50}\nSuccesful run docker container from image: {img_name}')
        except sub.CalledProcessError as ex:
            print(f'{"=" * 50}ERROR!{"=" * 50}\nSomething do wrong:', ex)
    else:
        print(f'Docker-container with name {con_name} already exist')


@wait_for(2)
def check_docker_container_ip(con_name:str) -> str:
    """
    :con_name: - name of docker-container
    Getting IP address of docker-containers
    """
    check_ip_docker_exec = "sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "
    total_exec = check_ip_docker_exec + con_name
    avaliable_containers = [con['NAMES'] for con in parse_docker_check_result(COMM_CHECK_CONTAINERS)]
    if con_name not in avaliable_containers:
        try:
            container_ip = sub.check_output(total_exec, shell=True).decode().strip()
            print(f'{"=" * 50}SUCCESS!{"=" * 50}\nSuccesful find out docker container IP from docker-container: {con_name}')
            return container_ip
        except sub.CalledProcessError as ex:
            print(f'{"=" * 51}ERROR!{"=" * 50}\nPerhabs some truble with docker: ', ex)
    else:
        print(f'Docker-container with name {con_name} not exist')


@wait_for(2)
def sind_data_to_config_json(data:dict, config_file:str, path_to_resource:str=None) -> None:
    path_to_resource = path_to_resource or ''
    path_to_config_file = os.path.join(path_to_resource, config_file)
    with open(path_to_config_file, 'w') as file:
        try:
            data_from_json = json.load(file)
        except UnsupportedOperation:
            data_from_json = {}

    data_from_json.update(data)
    with open(path_to_config_file, 'w') as file:
        json.dump(data_from_json, file)


@wait_for(2)
def copy_file(path_file_from:str, path_file_to:str) -> None:
    copy = sub.run(f'cp {path_file_from} {path_file_to}', shell=True)
    if copy.returncode == 0:
        print(f'{"=" * 50}SUCCESS!{"=" * 50}\nFile {path_file_from.split("/")[-1]} ssccessfull copied')
    else:
        print(f'{"=" * 51}ERROR!{"=" * 50}\nFile {path_file_from.split("/")[-1]} not copied or somethin else')


@wait_for(2)
def create_file_nginx_config(
            path_to_base_folder:str,
            template_file_name:str, 
            nginx_conf_file_name:str, 
            ip_1:str, 
            ip_2:str
            ):
    """
    take ip docker-containers and fill-ins him to the nginx configuration files
    """
    path_to_template_file = os.join(path_to_base_folder, template_file_name)
    with open(path_to_template_file, 'r') as file:
        template_form = file.read()

    nginx_conf = template_form.format(ip_1, ip_2)

    path_to_nginx_conf = os.path.join(path_to_base_folder, nginx_conf_file_name)
    with open(path_to_nginx_conf, 'w') as file:
        file.write(nginx_conf)
