#Cool Dogs Fetcher

A lightweight Flask app that fetches dog images, stores them in a temporary SQLite database, and serves them via a small web UI.

Architecture
	•	Flask web server (Python)
	•	SQLite database (auto-created per run)
	•	Simple HTML UI (served at /)
	•	Ephemeral data (reset each fetch)


 Endpoints
	•	/ – Web UI
	•	/image/fetch?x=N – Fetches N new images (resets DB)
	•	/image/<name> – Returns image #name (1...n, between 1 and 50)
	•	/image/last – Returns the most recent image

⸻

Run locally

pip install -r requirements.txt
python3 app1.py
# Open http://localhost:8000/

🐳 Run in Docker

docker compose build
docker compose up
# Open http://localhost:8000/

For the purpose of this app, no persistent volume: the SQLite database is rebuilt on every new fetch or container restart.
