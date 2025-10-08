from flask import Flask, request, jsonify, Response, abort, render_template
import sqlite3
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Fixed source image 
IMAGE_URL = "https://place.dog/300/200"

DB_PATH = "images.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            content_type TEXT,
            data BLOB NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    return conn

def save_image(name: str, data: bytes, content_type: str):
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO images (name, content_type, data, created_at) VALUES (?, ?, ?, ?)",
        (name, content_type, data, datetime.utcnow().isoformat(timespec="seconds") + "Z"),
    )
    conn.commit()
    conn.close()

# API REST endpoint to get images from DogStore
@app.get("/image/fetch")
def fetchadog():
    # How many images to fetch - between 1 and 50
    try:
        x = int(request.args.get("x", "5"))
    except ValueError:
        abort(400, "x must be an integer")
    if x < 1:
        abort(400, "x must be >= 1")
    if x > 50:
        abort(400, "x too large (max 50)")

    # Reset the table 
    conn = get_db()
    conn.execute("DELETE FROM images")
    conn.commit()
    conn.close()

    # Fetch and store
    for i in range(1, x + 1):
        try:
            r = requests.get(IMAGE_URL, timeout=15)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            status = getattr(e.response, "status_code", 502)
            abort(status, f"Upstream error: {status}")
        except requests.exceptions.RequestException as e:
            abort(502, f"Fetch failed: {e}")

        content_type = r.headers.get("Content-Type", "application/octet-stream")
        save_image(str(i), r.content, content_type)

    return jsonify({"status": "ok", "fetched": x})


@app.get("/image/<name>")
def get_image(name):
    conn = get_db()
    cur = conn.execute("SELECT content_type, data FROM images WHERE name = ?", (name,))
    row = cur.fetchone()
    conn.close()
    if not row:
        abort(404, f"No image named {name}")
    content_type, data = row
    return Response(data, mimetype=content_type, headers={"Content-Disposition": "inline"})

# API REST endpoint for the last image stored in the local DB
@app.get("/image/last")
def get_last_image():
    conn = get_db()
    cur = conn.execute("""
        SELECT content_type, data 
        FROM images 
        ORDER BY id DESC 
        LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()

    if not row:
        abort(404, "No images found in database")

    content_type, data = row
    return Response(
        data,
        mimetype=content_type,
        headers={"Content-Disposition": "inline"}
    )


@app.get("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # pip install flask requests
    app.run(host="0.0.0.0", port=8000, debug=True)