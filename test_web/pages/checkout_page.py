from playwright.sync_api import Page
from test_web.utils.logger import logger

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        # self.first_name = "input[name='firstname']"
        # self.last_name = "input[name='lastname']"
        # self.company = "input[name='company']"
        # self.street_address = "input[name='street[0]']"
        # self.city = "input[name='city']"
        # self.state_dropdown = "select[name='region_id']"
        # self.zip_code = "input[name='postcode']"
        # self.country_dropdown = "select[name='country_id']"
        # self.phone_number = "input[name='telephone']"
        self.first_shipping_method = "(//input[@type='radio' and contains(@name,'ko_unique')])[1]"
        self.next_button = "button.continue"

    # def fill_shipping_address(self, first, last, company, street, city, state, zipcode, country, phone):
    #     logger.info("Waiting for checkout shipping form to load...")
    #     self.page.wait_for_selector(self.first_name, timeout=20000)
    #     logger.info("Filling checkout shipping address")
    #     self.page.locator(self.first_name).fill(first)
    #     self.page.locator(self.last_name).fill(last)
    #     self.page.locator(self.company).fill(company)
    #     self.page.locator(self.street_address).fill(street)
    #     self.page.locator(self.city).fill(city)
    #     self.page.select_option(self.state_dropdown, label=state)
    #     self.page.locator(self.zip_code).fill(zipcode)
    #     self.page.select_option(self.country_dropdown, label=country)
    #     self.page.locator(self.phone_number).fill(phone)

    def select_first_shipping_method(self):
        logger.info("Selecting first shipping method")
        self.page.locator(self.first_shipping_method).click()

    def click_next(self):
        logger.info("Clicking Next to go to Payment step")
        next_btn = self.page.locator(self.next_button)
        next_btn.wait_for(state="visible", timeout=15000)
        next_btn.click()
        self.page.wait_for_selector("div.payment-group", timeout=20000)
        logger.info("Payment page loaded.")

    def click_place_order(self):
        from test_web.utils.logger import logger
        logger.info("Clicking Place Order button")
        place_order_btn = self.page.locator("button.action.primary.checkout")
        place_order_btn.wait_for(state="visible", timeout=15000)
        place_order_btn.click()

