from test_web.pages.login_page import LoginPage
from test_web.pages.search_page import SearchPage
from test_web.pages.checkout_page import CheckoutPage
from test_web.utils.logger import logger
from playwright.sync_api import expect

class KeywordActions:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.search_page = SearchPage(page)
        self.checkout_page = CheckoutPage(page)

    # --------------------
    # Generic helpers
    # --------------------
    def open_url(self, url):
        logger.info(f"Opening URL: {url}")
        self.page.goto(url, timeout=60000)

    def input_text(self, selector, value):
        logger.info(f"Filling input at {selector} with value: {value}")
        elem = self.page.locator(selector)
        elem.wait_for(state="visible", timeout=10000)
        elem.fill(value)

    def click_element(self, selector, wait_for_navigation=False):
        logger.info(f"Clicking element: {selector}")
        elem = self.page.locator(selector)
        elem.wait_for(state="visible", timeout=15000)
        elem.scroll_into_view_if_needed()
        if wait_for_navigation:
            with self.page.expect_navigation(timeout=15000):
                elem.click()
        else:
            elem.click()

    def assert_text(self, selector, expected_text):
        logger.info(f"Asserting text on {selector}")
        actual_text = self.page.inner_text(selector)
        if expected_text.lower() not in actual_text.lower():
            raise AssertionError(f"Expected '{expected_text}' in '{actual_text}'")

    # --------------------
    # Login flow
    # --------------------
    def login_as(self, email, password):
        logger.info("Performing login...")
        self.page.click("//a[contains(text(),'Sign In')]")
        self.page.wait_for_load_state('load', timeout=30000)
        self.page.wait_for_selector("#email", timeout=30000)
        self.page.fill("#email", email)
        self.page.wait_for_selector("#pass", timeout=30000)
        self.page.fill("#pass", password)
        login_btn = self.page.locator("button.action.login.primary[type='submit']")
        login_btn.wait_for(state="visible", timeout=30000)
        expect(login_btn).to_be_enabled(timeout=30000)
        login_btn.click()
        self.page.wait_for_load_state('load', timeout=30000)

    # --------------------
    # Search / product selection
    # --------------------
    def input_search_keyword(self, keyword):
        self.search_page.enter_search_keyword(keyword)

    def click_search_button(self):
        self.search_page.click_search_button()

    def assert_search_results_contains(self, expected_text):
        actual_text = self.search_page.get_search_results_header_text()
        if expected_text.lower() not in actual_text.lower():
            raise AssertionError(f"Expected '{expected_text}' but got '{actual_text}'")

    def select_adrienne_trek_jacket(self):
        self.search_page.select_adrienne_trek_jacket()

    def select_size_small(self):
        self.search_page.select_size_small()

    def select_color_blue(self):
        self.search_page.select_color_blue()

    def add_to_cart(self):
        self.search_page.add_to_cart()

    def click_cart_icon(self):
        self.search_page.click_cart_icon()

    def click_proceed_to_checkout(self):
        self.search_page.click_proceed_to_checkout()

    # --------------------
    # Checkout / shipping flow
    # --------------------
    # def fill_checkout_shipping_address(self, first, last, company, street, city, state, zipcode, country, phone):
    #     self.checkout_page.fill_shipping_address(first, last, company, street, city, state, zipcode, country, phone)

    def select_first_shipping_method(self):
        self.checkout_page.select_first_shipping_method()

    def click_next_button(self):
        self.checkout_page.click_next()

    # --------------------
    # Payment / order confirmation
    # --------------------
    def click_place_order(self):
        self.checkout_page.click_place_order()

