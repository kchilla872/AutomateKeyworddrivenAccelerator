from .base_page import BasePage
from test_web.utils.logger import logger

class LoginPage(BasePage):
    def login(self, email, password):
        logger.info("Starting login process")

        # Click the 'Sign In' link to navigate to login page
        self.page.click("//a[contains(text(),'Sign In')]")
        self.page.wait_for_load_state('load')
        logger.info("Navigated to Sign In page")

        # Wait for email input and fill email
        self.page.wait_for_selector("#email", timeout=15000)
        self.page.fill("#email", email)
        logger.info(f"Entered email: {email}")

        # Wait for password input and fill password
        self.page.wait_for_selector("#pass", timeout=15000)
        self.page.fill("#pass", password)
        logger.info("Entered password")

        # Locate and wait for the 'Sign In' button, then click it
        sign_in_btn = self.page.locator("//button[@type='submit' and contains(text(), 'Sign In')]")
        sign_in_btn.wait_for(state="visible", timeout=15000)
        sign_in_btn.wait_for(state="enabled", timeout=15000)
        sign_in_btn.click()
        logger.info("Clicked Sign In button")

        # Wait for page to load fully after login
        self.page.wait_for_load_state('load', timeout=30000)
        logger.info("Login process complete")
