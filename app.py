
# from routes import app  # import your Flask app from routes.py
# import threading
# import time
# import requests

# def run_app():
#     app.run(host="127.0.0.1", port=5000)

# # Start Flask in a separate thread
# threading.Thread(target=run_app, daemon=True).start()

# # Wait until the server is ready
# for i in range(20):
#     try:
#         r = requests.get("http://127.0.0.1:5000")
#         if r.status_code == 200:
#             print("READY")
#             break
#     except:
#         time.sleep(1)

# # Keep the script alive
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Flask server stopping...")



from routes import app  # import your Flask app from routes.py
import threading
import time
import requests
import logging
import os

# -------------------------------
# Setup logging
# -------------------------------
log_file = os.path.join(os.getcwd(), "flask_error.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Optional: also log to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# -------------------------------
# Error handling for all routes
# -------------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    logging.exception("Unhandled Exception: ")
    return "Internal Server Error", 500

# -------------------------------
# Function to run Flask
# -------------------------------
def run_app():
    try:
        # use_reloader=False prevents multiple processes
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logging.exception("Flask failed to start")
        raise e

# -------------------------------
# Start Flask in a separate thread
# -------------------------------
threading.Thread(target=run_app, daemon=True).start()

# -------------------------------
# Wait until server is ready
# -------------------------------
server_ready = False
for i in range(30):  # wait up to 30 seconds
    try:
        r = requests.get("http://127.0.0.1:5000")
        if r.status_code == 200:
            print("READY")
            print("Flask server is running at: http://127.0.0.1:5000")
            server_ready = True
            break
    except Exception as e:
        logging.debug(f"Server not ready yet: {e}")
        time.sleep(1)

if not server_ready:
    logging.error("Flask did not start in time!")
    raise RuntimeError("Flask server failed to start")

# -------------------------------
# Keep the script alive
# -------------------------------
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Flask server stopping...")
