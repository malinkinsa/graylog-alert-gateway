# Graylog Alert Gateway

Web based application designed to integrate graylog with different IRP systems.

- [Graylog Alert Gateway](#Graylog-Alert-Gateway)
  - [Description](#Description) 
  - [Environment](#Environment)
  - [Setup](#setup)
    - [Native](#native)
    - [Docker & Docker-compose](#docker--docker-compose)
      - [Pre-built](#pre-built)
      - [Your own](#your-own)
  - [To Do](#To-Do)

## Description
This application allows you to deliver graylog alert data to the following irp systems:
- [TheHive4](https://thehive-project.org)

And to Telegram (Optional)

## Environment

This app has been tested with the following versions:
- Python 3.9
- Graylog 4.2.2
- TheHive4 4.1.16

## Setup

### Native
- Create non root user:
```shell
sudo adduser --disabled-password gateway && \
sudo su - gateway
```

- Checkout the code:
```shell
git clone git@github.com:malinkinsa/graylog-alert-gateway.git
```

- Setup Virtual Environment:
```shell
virtualenv --python=python3 gateway-env && \
source gateway-env/bin/activate
```

- Install python requirements:
```shell
pip3 install --no-cache-dir --upgrade pip --user && \
pip3 install --no-cache-dir -r requirements.txt --user
```

- Setup the app via config.ini:
```shell
vi graylog-alert-gateway/config.ini
```

- Logout from user gateway

- Create init.d file:
```shell
sudo vi /etc/systemd/system/graylog-alert-gateway.service

[Unit]
Description=graylog-alert-gateway
After=multi-user.target

[Service]
Type=idle
ExecStart=/home/gateway/gateway-env/bin/python3 /home/gateway/graylog-alert-gateway/launch.py

# Connects standard output to journal
StandardOutput=journal

# Connects standard error to journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

- Reload init.d configuration:
```shell
sudo systemctl daemon-reload
```

- Launch app:
```shell
sudo systemctl start graylog-alert-gateway.service
```

### Docker & Docker-compose

#### Pre-built
Supported tags

```latest```

- Pull image:
```shell
docker pull malinkinsa/graylog-alert-gateway:latest
``` 
 - Download and configure ```config.ini```:
```shell
wget https://raw.githubusercontent.com/malinkinsa/graylog-alert-gateway/master/config.ini && \
vi vonfig.ini
```

- Start docker container:
```shell
docker run -d \
--name graylog-alert-gateway \
-v config.ini:/opt/graylog-alert-gateway/config.ini \
-p 8000:8000 \
malinkinsa/graylog-alert-gateway:latest
```

#### Your own

- Checkout the code:
```shell
git clone git@github.com:malinkinsa/graylog-alert-gateway.git
```

- Configure ```config.ini```:
```shell
cd graylog-alert-gateway && \
vi config.ini
```

- Build your own container:
```shell
docker build -t name:tag . 
```

- Start docker container:
```shell
docker run -d \
--name graylog-alert-gateway \
-p 8000:8000 \
name:tag
```

## To Do
- [x] Docker support;
- [x] README about Setup;
  - [x] Native;
  - [x] Dockerized;