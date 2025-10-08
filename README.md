# Cool Dogs Fetcher

A lightweight Flask app that fetches dog images, stores them in a temporary SQLite database, and serves them via a small web UI.

Architecture
- **Flask (Python)** – Web API & UI  
- **SQLite** – Local ephemeral storage (auto-created)  
- **Frontend** – Minimal HTML + JS served at `/`


Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Web UI |
| `/image/fetch?x=N` | GET | Fetch N new images (resets DB) |
| `/image/<name>` | GET | Retrieve stored image by name |
| `/image/last` | GET | Retrieve the latest stored image |

## Download app repo

```
git clone https://github.com/andreworanskyi/cool-dogs-fetcher.git
cd cool-dogs-fetcher
```

## Run locally

```
apt-get install git
git clone https://github.com/WerNad99/cool-dogs-fetcher.git

pip install -r requirements.txt
python app1.py
``` 
- Open http://localhost:80/ (standart HTTP - you will only be able to use it as a root user/won't work with sudo; in case this happens, feel free to adapt the port accordingly)

## Run in Docker
``` 
docker compose build
docker compose up
``` 
- Open http://localhost:80/

For the purpose of this app, no persistent volume: the SQLite database is rebuilt on every new fetch or container restart.

## EC2 User Data

In case you would like to test this app on your EC2 instance, please configure a Security Group allowing inbound trafic on the port 80 (HTTP) and use the following User Data before launch:
```
#!/bin/bash
dnf update -y
dnf install -y docker git
systemctl enable --now docker

git clone https://github.com/WerNad99/cool-dogs-fetcher.git /opt/app
cd /opt/app
curl -L https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker compose up -d

```
