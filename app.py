
# from routes import app  # import your Flask app from routes.py
# import threading
# import time
# import requests

# def run_app():
#     app.run(host="127.0.0.1", port=5000)

# # Start Flask in a separate thread
# threading.Thread(target=run_app).start()

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

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, render_template, request
import traceback
import nltk

# Ensure NLTK resources are available
nltk.download("stopwords", quiet=True)

app = Flask(__name__)

# ----------------------------
# Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            text = request.form.get("pasted_text")
            if not text:
                return "No text provided", 400

            # --- Example processing ---
            # Replace this with your actual analysis logic
            result = text.upper()  # simple placeholder
            return render_template("index.html", result=result)

        except Exception as e:
            # Print traceback for debugging
            print(traceback.format_exc())
            return f"Internal Server Error: {str(e)}", 500

    # GET request
    return render_template("index.html")


# ----------------------------
# Function to run app (for threads or background)
# ----------------------------
def run_app():
    app.run(host="0.0.0.0", port=5000, debug=True)


# ----------------------------
# Only run app when executing python app.py directly
# ----------------------------
if __name__ == "__main__":
    run_app()
