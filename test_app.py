
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# class MyAppTest(unittest.TestCase):

#     def setUp(self):
#         # Setup Chrome browser
#         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         self.driver.get("http://127.0.0.1:5000")
#         self.wait = WebDriverWait(self.driver, 10)  # Explicit wait

#     def test_homepage_title(self):
#         # Check if the homepage title is correct
#         self.assertIn("Document Analyzer", self.driver.title)

#     def test_textarea_submit(self):
#         # Locate the textarea
#         text_area = self.wait.until(
#             EC.presence_of_element_located((By.NAME, "pasted_text"))
#         )

#         # Enter some text
#         text_area.send_keys("This is a test document.")

#         # Locate the Analyze button and click
#         analyze_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
#         analyze_button.click()

#         # You can optionally wait for the page to load after submission
#         # For now, just check that the new page title is something expected (if applicable)
#         # For example, if the analyze page title changes:
#         # self.assertIn("Analysis Result", self.driver.title)

#     def tearDown(self):
#         # Close the browser
#         self.driver.quit()

#     def test_textarea_submit(self):
#     # Locate the textarea
#         text_area = self.wait.until(
#             EC.presence_of_element_located((By.NAME, "pasted_text"))
#         )

#         # Enter some text
#         text_area.send_keys("This is a test document.")

#         # --- Replace your current button click with this ---
#         analyze_button = self.wait.until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))
#         )

#         # Scroll into view (optional)
#         self.driver.execute_script("arguments[0].scrollIntoView();", analyze_button)

#         # Click the button
#         analyze_button.click()

# if __name__ == "__main__":
#     unittest.main()


import unittest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from app import app  # Import your Flask app

# --- Start Flask in a background thread ---
def run_flask():
    app.run(port=5000)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Give Flask some time to start
time.sleep(5)

class MyAppTest(unittest.TestCase):

    def setUp(self):
        # Setup headless Chrome browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("http://127.0.0.1:5000")

    def test_homepage_title(self):
        self.assertIn("Document Analyzer", self.driver.title)

    def test_textarea_submit(self):
        # Locate textarea and type
        text_area = self.wait.until(
            EC.presence_of_element_located((By.NAME, "pasted_text"))
        )
        text_area.send_keys("This is a test document.")

        # Locate and click Analyze button
        analyze_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", analyze_button)
        analyze_button.click()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
