# Cool Dogs Fetcher

A lightweight Flask app that fetches dog images, stores them in a temporary SQLite database, and serves them via a small web UI.

Architecture
- **Flask (Python)** – Web API & UI  
- **SQLite** – Local ephemeral storage (auto-created)  
- **Frontend** – Minimal HTML + JS served at `/`


🔗 Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Web UI |
| `/image/fetch?x=N` | GET | Fetch N new images (resets DB) |
| `/image/<name>` | GET | Retrieve stored image by name |
| `/image/last` | GET | Retrieve the latest stored image |

⸻

## Run locally

```
pip install -r requirements.txt
python app1.py
``` 
- Open http://localhost:8000/

## Run in Docker
``` 
docker compose build
docker compose up
``` 
- Open http://localhost:8000/

For the purpose of this app, no persistent volume: the SQLite database is rebuilt on every new fetch or container restart.
