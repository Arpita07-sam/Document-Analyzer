
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class MyAppTest(unittest.TestCase):

    
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome without GUI
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                    options=chrome_options)
        self.driver.get("http://127.0.0.1:5000")
        self.wait = WebDriverWait(self.driver, 10)


    # def setUp(self):
    #     # Setup Chrome browser
    #     self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #     self.driver.get("http://127.0.0.1:5000")
    #     self.wait = WebDriverWait(self.driver, 10)  # Explicit wait

    def test_homepage_title(self):
        # Check if the homepage title is correct
        self.assertIn("Document Analyzer", self.driver.title)

    def test_textarea_submit(self):
        # Locate the textarea
        text_area = self.wait.until(
            EC.presence_of_element_located((By.NAME, "pasted_text"))
        )

        # Enter some text
        text_area.send_keys("This is a test document.")

        # Locate the Analyze button and click
        analyze_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
        analyze_button.click()

        # You can optionally wait for the page to load after submission
        # For now, just check that the new page title is something expected (if applicable)
        # For example, if the analyze page title changes:
        # self.assertIn("Analysis Result", self.driver.title)

    def tearDown(self):
        # Close the browser
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

