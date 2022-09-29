import subprocess as sub
import os
import json
from io import UnsupportedOperation
import time
import functools
import re

from . import constance as co
from docker_installer.main import DEBUG_CONTROL

def wait_for(seconds):
    """
    func decorator for use time.slip() on used functon end control
    for execute decorated functions if DEBUG_CONTROL == True
    """
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if DEBUG_CONTROL:
                print(f'Executed function: {func.__name__}\nUsing arguments: {args, kwargs}\n' )
            time.sleep(seconds)
            result = func(*args, **kwargs)
            return result
        return inner
    return decorator


@wait_for(2)
def check_host_ip():
    """
    Check IP of host
    """
    print('Start function for checking IP of host')
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
    print('Start function for install dependencies for applications')
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
    print('Start function for create certificates')
    path_to_keys = os.path.join(path_to_resource, 'keys')
    if not os.path.exists(path_to_keys):
        os.mkdir(os.path.join(path_to_resource, 'keys'))
    cert_command = sub.run(co.COM_CERT_CREATE.format(path_to_resource, domain_name), shell=True)
    path_to_cert = os.path.join(path_to_keys, 'bot_cert.pem')
    path_to_key = os.path.join(path_to_keys, 'cert_pkey.key')
    if cert_command.returncode == 0 and os.path.exists(path_to_cert) and os.path.exists(path_to_key):
        print(f'{co.SUCCESS}\nSuccessful create certificate with key for domainname: ', domain_name)
    else:
        print(f'{co.ERROR}\n, {cert_command}')


@wait_for(2)
def parse_docker_check_result(command:str) -> list:
    """
    :command: - docker command for take a list of items
    for example: 'sudo docker ps'
    """
    print(f'Start function for parse docker contains information for {command}')
    data_str = sub.check_output(command, shell=True).decode()
    list_data_split = [value for value in data_str.split('\n') if value]
    list_data = [re.split(r'\s{2,}', row) for row in list_data_split]
    dict_data = []
    for list_ in list_data[1:]:
       list_.insert(-1, []) if len(list_) < len(list_data[0]) else list_
       dict_data.append({k:w for (k, w) in zip(list_data[0], list_)})
    return dict_data


@wait_for(2)
def create_docker_volume(path_to_resource:str, mongo_db_folder:str, docker_volume_name:str)-> None:
    """
    Create docker-volume with binding to folder
    """
    print(f'Start function for docker volume created vith name {docker_volume_name}')
    mongo_db_folder_path = os.path.join(path_to_resource, mongo_db_folder)
    if not os.path.exists(os.path.join(path_to_resource, mongo_db_folder)):
        os.mkdir(mongo_db_folder_path)
    aval_vilumes = [volume.get(co.NAMES[co.VOL]) for volume in parse_docker_check_result(co.COM_CHECK[co.VOL])]
    if docker_volume_name not in aval_vilumes:
        try:
            volume = sub.check_output(co.COM_DOK_VOLUME_CREATE.format(docker_volume_name, mongo_db_folder_path), shell=True)
            print(f'{co.SUCCESS}\nDocker volume {docker_volume_name} created')
        except sub.CalledProcessError as ex:
            print(f'{co.ERROR}\nSomething wrong: {ex}')
    else:
        print(f'{co.ERROR}\nDocker volume {docker_volume_name} allready exist')


@wait_for(2)
def create_docker_image( image_name:str, path_to_dokerfile:str):
    """
    Created docker image
    """
    print(f'Start function for create docker image {image_name}')
    create_image_command = f'sudo docker build -t {image_name} {path_to_dokerfile}'
    aval_images = [image.get(co.NAMES[co.IMG]) for image in parse_docker_check_result(co.COM_CHECK[co.IMG])]
    if image_name not in aval_images:
        try:
            sub.check_output(create_image_command, shell=True)
            print(f'{co.SUCCESS}\nDocker image: {image_name} successful created')
        except sub.CalledProcessError as ex:
            print(f'{co.ERROR}\nSomething do wrong:', ex)
    else:
        print(f'Docker-image with name {image_name} already exist')
        

@wait_for(2)
def run_docker_container(con_name:str=None, p:str=None, v:str=None, *, img_name:str) -> None:
    print(f'Start function for run docker-container vith name: {con_name} from image {img_name}')
    con_name = con_name or ''
    p = p or ''
    v = v or ''
    avaliable_containers = [con.get(co.NAMES[co.CON]) for con in parse_docker_check_result(co.COM_CHECK[co.CON])]
    if con_name not in avaliable_containers:
        try:
            sub.run(co.COM_DOK_RUN_CON.format(con_name=con_name, p=p, v=v, img_name=img_name), shell=True)
            print(f'{co.SUCCESS}\nSuccesful run docker container: {con_name.split()[-1]} from image: {img_name}')
        except sub.CalledProcessError as ex:
            print(f'{co.ERROR}\nSomething do wrong:', ex)
    else:
        print(f'Docker-container with name {con_name.split()[-1]} already exist')


@wait_for(2)
def check_docker_container_ip(con_name:str) -> str:
    """
    :con_name: - name of docker-container
    Getting IP address of docker-containers
    """
    print(f'Start function checking IP of docker-container vith name: {con_name}')
    total_exec = co.COMM_DOCK_IP + con_name
    avaliable_containers = [con.get('NAMES') for con in parse_docker_check_result(co.COM_CHECK[co.CON])]
    if con_name in avaliable_containers:
        try:
            container_ip = sub.check_output(total_exec, shell=True).decode().strip()
            print(f'{co.SUCCESS}\nSuccesful find out IP {container_ip} of docker-container: {con_name}')
            return container_ip
        except sub.CalledProcessError as ex:
            print(f'{co.ERROR}\nPerhabs some truble with docker: ', ex)
    else:
        print(f'Docker-container with name {con_name} not exist')


@wait_for(2)
def sind_data_to_config_json(data:dict, config_file:str, path_to_resource:str=None) -> None:
    print(f'Sind configuration data on config file: {config_file}')
    path_to_resource = path_to_resource or ''
    path_to_config_file = os.path.join(path_to_resource, config_file)
    with open(path_to_config_file, 'w') as file:
        try:
            data_from_json = json.load(file)
        except UnsupportedOperation:
            data_from_json = {}

    data_from_json.update(data)
    with open(path_to_config_file, 'w') as file:
        try:
            json.dump(data_from_json, file)
            print(f'{co.SUCCESS}\ndata successfull sind to {path_to_config_file}')
        except IOError as ex:
            print(f'{co.ERROR}\ndata not sind to {path_to_config_file}\nPerhabs some truble with path: ', ex)


@wait_for(2)
def copy_file(path_file_from:str, path_file_to:str) -> None:
    print(f'Start copy file:\nFROM: {path_file_from}\n{path_file_to}')
    copy = sub.run(f'cp {path_file_from} {path_file_to}', shell=True)
    if copy.returncode == 0:
        print(f'{co.SUCCESS}\nFile {path_file_from.split("/")[-1]} saccessfull copied')
    else:
        print(f'{co.ERROR}\nFile {path_file_from.split("/")[-1]} not copied or somethin else')


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
    print(f'Start to create file nginx.config')
    path_to_template_file = os.path.join(path_to_base_folder, template_file_name)
    with open(path_to_template_file, 'r') as file:
        template_form = file.read()

    nginx_conf = template_form.format(ip_1, ip_2)
    path_to_nginx_conf = os.path.join(path_to_base_folder, nginx_conf_file_name)

    with open(path_to_nginx_conf, 'w') as file:
        file.write(nginx_conf)


def check_file_exist(path_to_file:str) -> None:
    return os.path.isfile(path_to_file)


@wait_for(2)
def remove_file(path_to_file)-> None:
    print(f'Start to file remove {path_to_file}')
    if check_file_exist(path_to_file):
        try:
            sub.run(f'sudo rm {path_to_file}', shell=True)
            print(f'{co.SUCCESS}\nRemove file {path_to_file.split("/")[-1]}')
        except sub.CalledProcessError as ex:
            print(f'{co.ERROR}\nRemove file {path_to_file.split("/")[-1]} not suxessful')


@wait_for(2)
def rm_from_docker(command:str, arr):
    print('Start removing objects from Docker-repository')    
    victims_of_deletion = ' '.join(arr)
    if victims_of_deletion:
        try:
            sub.run(command.format(victims_of_deletion), shell=True)
            print(f'{co.SUCCESS}\nSuccessful remove {victims_of_deletion}')
        except sub.CalledProcessError as ex:
            print(f'{co.ERROR}\nFailure remove {victims_of_deletion}')
    else:
        print("Have not victims to remove")
