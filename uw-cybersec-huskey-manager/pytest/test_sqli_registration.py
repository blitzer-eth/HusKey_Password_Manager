import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestSQLiRegistration():
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)

    def teardown_method(self, method):
        self.driver.quit()

    def test_registration_sqli_neutralization(self):
        # 1. Navigate to the page
        self.driver.get("http://localhost/users/request_account.php")

        # 2. Wait for page to fully load
        wait = WebDriverWait(self.driver, 15)

        # DEBUG: Print current URL and page title to confirm we landed on the right page
        print(f"\n[DEBUG] Current URL: {self.driver.current_url}")
        print(f"[DEBUG] Page title: {self.driver.title}")

        # 3. Try multiple strategies to locate the username field
        username_field = None
        selectors = [
            (By.ID, "username"),
            (By.NAME, "username"),
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.CSS_SELECTOR, "input[placeholder*='user' i]"),
            (By.XPATH, "//input[contains(@id,'user') or contains(@name,'user')]"),
        ]

        for by, selector in selectors:
            try:
                username_field = wait.until(EC.presence_of_element_located((by, selector)))
                print(f"[DEBUG] Found username field using: ({by}, '{selector}')")
                break
            except TimeoutException:
                print(f"[DEBUG] Selector failed: ({by}, '{selector}')")

        # DEBUG: If still not found, dump page source to help diagnose
        if username_field is None:
            print(f"[DEBUG] Page source snippet:\n{self.driver.page_source[:3000]}")
            pytest.fail(
                "Could not locate a username input field on the registration page. "
                "Check the page source printed above to find the correct selector."
            )

        # 4. Input SQLi payload
        sqli_user = "hacker' -- "
        username_field.clear()
        username_field.send_keys(sqli_user)

        # Locate and fill password field with fallback selectors
        password_field = None
        password_selectors = [
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
        ]
        for by, selector in password_selectors:
            try:
                password_field = self.driver.find_element(by, selector)
                print(f"[DEBUG] Found password field using: ({by}, '{selector}')")
                break
            except Exception:
                print(f"[DEBUG] Password selector failed: ({by}, '{selector}')")

        assert password_field is not None, "Could not locate a password field."
        password_field.clear()
        password_field.send_keys("password123")

        # Submit — try common submit selectors
        submit_selectors = [
            (By.CSS_SELECTOR, ".btn"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//button[contains(text(),'Register') or contains(text(),'Submit')]"),
        ]
        submitted = False
        for by, selector in submit_selectors:
            try:
                self.driver.find_element(by, selector).click()
                submitted = True
                print(f"[DEBUG] Clicked submit using: ({by}, '{selector}')")
                break
            except Exception:
                continue

        assert submitted, "Could not find or click a submit button."

        time.sleep(2)
        print(f"[DEBUG] Post-submit URL: {self.driver.current_url}")

        # 5. Assert the app handled the payload safely (no crash/500 error)
        page_source = self.driver.page_source.lower()
        assert "500" not in self.driver.title, "Server returned a 500 error — possible SQLi vulnerability."
        assert "sql" not in page_source or "error" not in page_source, \
            "Page may be leaking SQL error details."

        stayed_on_form = self._element_exists(By.CSS_SELECTOR, "input")
        went_to_login = "login" in self.driver.current_url.lower()

        assert stayed_on_form or went_to_login, \
            f"Unexpected redirect after SQLi attempt: {self.driver.current_url}"

        print("Registration SQLi neutralized successfully.")

    def _element_exists(self, by, selector):
        """Helper: returns True if element is present, False otherwise."""
        try:
            self.driver.find_element(by, selector)
            return True
        except Exception:
            return False