Application that controls the installation and connection of all program components in docker containers.

Host and environment configuration file to successfully install and run aiogram-bot with serving systems.
such as nginx-server (serving bot-webhook and bot-API), mongo-db as databases for serving Telegram-Bot,
and Bot-API for accessing and working with the database. The build architecture consists of four Docker containers, for each individual system and a docker volume to store mongo container data:
  - aiogram-bot + webhook
  - API-app;
  - mongo-db;
  - nginx;
  - docker-volume.   

Configuration and installation consists of 9 steps:
1) Installing the docker program on the host;
2) Creation of an ssl certificate and a key to it;
3) Check if docker-volume has already been created with the desired name. If not, create
docker-volume and bind it to the specified directory;
4) Starting a container with mongo-db. Attaching a docker volume.
5) Specify and write down the IP address of the docker container from mongo-DB;
6) Creating a docker image using the docker-mongodb IP address and running the docker container using the Bot-API application;
7) Creating a docker image using the docker-mongodb IP address and running the docker container using the Bot application;
8) Identification of the IP addresses assigned to the docker containers of the Bot application and API application, and the creation of an nginx configuration file using the above IP addresses;
9) Creating an nginx image with loading an ssl certificate and a key to it and connecting the configuration file.
10) Run the docker container with nginx

At the end of each stage, its execution is checked, and if an error is detected, the installation process signals at which stage the error occurred. When starting the application, the user will be prompted to clear all or part of the Docker repository from containers, images, and volume.

Download on host (for example aws instance) and run main.py
After install all containers:

Telegrambot - @NewReminderBot
API - http://<hostname or ip>/api

Structure

base
  |

   ------ nginx.conf
   ------ nginx
   ------ cofig.json
   ------ executer_docker_commands.txt
   ------ installer.py
app_bot
   |
    ------ Dockerfile
    ------ Bot
app_api
   |
    ------ Dockerfile
    ------ api
nginx
  |
   ------ Dockerfile
main.py
readme.md   
