import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestSQLInjectionLogin():
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
    
    def teardown_method(self, method):
        self.driver.quit()
    
    def test_sqli_bypass_attempt(self):
        self.driver.get("http://localhost/login.php")
        
        # Payload: ' OR 1=1 --
        # This attempts to bypass the login logic
        self.driver.find_element(By.ID, "username").send_keys("' OR 1=1 --")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        
        time.sleep(2)
        current_url = self.driver.current_url.lower()
        
        # PROOF OF REMEDIATION:
        # If the attack is blocked, we stay on the login page.
        assert "login" in current_url, "VULNERABILITY: SQL Injection bypassed the login page!"
        
        # Optional: Check for the alert message safely
        try:
            # Changed CLASS_MESSAGE to CLASS_NAME
            error_msg = self.driver.find_element(By.CLASS_NAME, "alert").text
            assert "Invalid" in error_msg or "Error" in error_msg
        except:
            print("Stayed on login page. SQLi blocked.")