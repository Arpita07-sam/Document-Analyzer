
from routes import app  # import your Flask app from routes.py
import threading
import time
import requests

def run_app():
    app.run(host="127.0.0.1", port=5000)

# Start Flask in a separate thread
threading.Thread(target=run_app).start()

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# from routes import app  # Import your Flask app
# from waitress import serve

# import time
# import requests
# import sys
# import os

# # Use absolute paths for logging
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOG_OUT = os.path.join(BASE_DIR, "flask_stdout.txt")
# LOG_ERR = os.path.join(BASE_DIR, "flask_stderr.txt")

# # def run_app():
# #     # Jenkins-friendly: no debug, no reloader
# #     serve(app, host="0.0.0.0", port=5000) #debug=False, use_reloader=False, threaded=True)

# if __name__ == "__main__":
#     serve(app, host="0.0.0.0", port=5000)


# # # Start Flask in a daemon thread
# # flask_thread = threading.Thread(target=, daemon=True)
# # flask_thread.start()

# # Wait until the server is ready
# server_ready = False
# for i in range(30):  # wait up to 30 seconds
#     try:
#         r = requests.get("http://127.0.0.1:5000/health")  # /health route should be in routes.py
#         if r.status_code == 200:
#             print("✅ Flask server is READY!")
#             server_ready = True
#             break
#     except requests.exceptions.ConnectionError:
#         time.sleep(1)

# if not server_ready:
#     print("❌ Flask did not start in time.")
#     sys.exit(1)

# # Keep script alive
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("Flask server stopping...")



