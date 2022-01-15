# Graylog Alert Gateway

Web based application designed to integrate graylog with different IRP systems.

- [Graylog Alert Gateway](#Graylog-Alert-Gateway)
  - [Description](#Description) 
  - [Environment](#Environment)
  - [Setup](#setup)
    - [Native](#native)
    - [Docker & Docker-compose](#docker--docker-compose)
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
```
sudo adduser --disabled-password gateway
sudo su - gateway
```

- Checkout the code:
```
git clone git@github.com:malinkinsa/graylog-alert-gateway.git
```

- Setup Virtual Environment:
```
virtualenv --python=python3 gateway-env
source gateway-env/bin/activate
```

- Install python requirements:
```
pip3 install --no-cache-dir --upgrade pip --user
pip3 install --no-cache-dir -r requirements.txt --user
```

- Setup the app via config.ini:
```
vi graylog-alert-gateway/config.ini
```

- Logout from user gateway

- Create init.d file:
```
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
```
sudo systemctl daemon-reload
```

- Launch app:
```
sudo systemctl start graylog-alert-gateway.service
```

### Docker & Docker-compose

## To Do
- [ ] Docker support;
- [ ] README about Setup;
  - [ ] Native;
  - [ ] Dockerized;