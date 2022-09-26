A file that controls the installation and connection of all program components in docker containers

Host and environment configuration file to successfully install and run aiogram-bot, with serving systems
such as nginx-server (serving bot-webhook and bot-API), mongo-db as databases for serving Telegram-Bot,
and Bot-API to access and work with the database. The construction architecture consists of four Docker containers, for each individual system and docker-volume, for storing mongo-container data:
  - aiogram-bot + webhook
  - API-app;
  - mongo-db;
  - nginx;
  - docker-volume.   

Setup and installation consists of 9 stages:
1) Installation of the docker program on the host;
2) Creating an ssl certificate and key to it;
3) Checking whether a docker-volume with the required name is already created. If not - create a 
docker-volume and bind it to the specified directory;
4) Starting a container with mongo-db. Connecting docker-volume.
5) We specify and record the IP-address of docker-container from mongo-DB;
6) Creating a docker-image with use the IP-address of docker-mongodb and starting the docker-container with Bot-API-app;
7) Creating a docker-image with use the IP-address of docker-mongodb and starting the docker-container with Bot-app;
8) Identification of IPs assigned to Bot-app and API-app docker containers and creation of nginx configuration file using the above IP addresses;
9) Creating an nginx image with uploading the ssl-certificate and key to it and connecting the configuration file.
10) Launch docker container with nginx

At the end of each stage, there is a check of its execution, and if an error is detected, the installation process is interrupted and it is indicated at which stage the error occurred. In the case of dust, the user will be prompted to remove all running containers, depending on the stage at which the installation was completed.

app template

base
  |
   ------ keys --------------------------
   ------ nginx.conf                     |--- cert_pkey.key
   ------ nginx                          |--- bot_cert.pem
   ------ cofig.json
   ------ executer_docker_commands.txt
   ------ installer.py
app_bot
   |
    ------ Dockerfile
app_api
   |
    ------ Dockerfile
nginx
  |
   ------ Dockerfile
main.py
readme.md   
