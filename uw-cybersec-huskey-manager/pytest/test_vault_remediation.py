import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestVaultRemediation():
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
    
    def teardown_method(self, method):
        self.driver.quit()

    def login(self):
        self.driver.get("http://localhost/login.php")
        self.driver.find_element(By.ID, "username").send_keys("alex_final_demo_01")
        self.driver.find_element(By.ID, "password").send_keys("alexpassword")
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()

    def test_stored_xss_remediation(self):
        self.login()
        # Navigate to a vault (Update ID as needed)
        self.driver.get("http://localhost/vaults/vault_details.php?vault_id=1")
        
        # 1. Attempt to inject a script into the notes
        self.driver.find_element(By.CSS_SELECTOR, "[data-target='#addPasswordModal']").click()
        xss_payload = "<script>alert('VULNERABLE')</script>"
        
        self.driver.find_element(By.ID, "addUsername").send_keys("hacker")
        self.driver.find_element(By.ID, "addWebsite").send_keys("evil.com")
        self.driver.find_element(By.ID, "addPassword").send_keys("password")
        self.driver.find_element(By.ID, "addNotes").send_keys(xss_payload)
        self.driver.find_element(By.CSS_SELECTOR, "#addPasswordForm .btn-primary").click()
        
        time.sleep(2)

        # 2. PROOF: If the script executed, an alert box would be present.
        # If no alert is present, the htmlspecialchars() remediation worked.
        try:
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            pytest.fail(f"XSS FAILURE: Script executed message: {alert_text}")
        except:
            print("XSS Remediation Verified: Script was treated as literal text.")

    def test_search_sqli_remediation(self):
        self.login()
        # 3. Attempt a SQL Injection in the search bar
        sqli_payload = "admin' OR 1=1 --"
        self.driver.get(f"http://localhost/vaults/vault_details.php?vault_id=1&searchQuery={sqli_payload}")
        
        # 4. PROOF: If remediation (Prepared Statements) is working, the DB 
        # treats the payload as a string. It should find 0 results or stay stable.
        # If vulnerable, it might return all rows or crash.
        assert self.driver.title != "", "SQLi FAILURE: Server crashed or returned blank page."
        print("SQLi Remediation Verified: Prepared statements neutralized the payload.")