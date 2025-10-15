
from routes import app  # import your Flask app from routes.py
import threading
import time
import requests

def run_app():
    app.run(host="127.0.0.1", port=5000)

# Start Flask in a separate thread
threading.Thread(target=run_app, daemon=True).start()

# Wait until the server is ready
for i in range(20):
    try:
        r = requests.get("http://127.0.0.1:5000")
        if r.status_code == 200:
            print("READY")
            break
    except:
        time.sleep(1)

# Keep the script alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Flask server stopping...")




