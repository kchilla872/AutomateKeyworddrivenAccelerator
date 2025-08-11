from playwright.sync_api import Page
from test_web.utils.logger import logger

class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = "#search"
        self.search_button = '//*[@id="search_mini_form"]/div[2]/button'
        self.search_results_header = "h1.page-title span.base[data-ui-id='page-title-wrapper']"

        # Product-specific selectors
        self.product_link = "(//li[contains(@class,'product-item')])[1]//a[contains(@class,'product-item-link')]"
        self.size_small = '//*[@id="option-label-size-143-item-167"]'
        self.color_blue = '//*[@id="option-label-color-93-item-56"]'
        self.add_to_cart_button = "//button[@id='product-addtocart-button']"
        self.cart_success_message = "div.message-success div"
        self.cart_icon = "//div[contains(@class,'minicart-wrapper')]//a[contains(@class,'showcart')]//span[contains(@class,'counter qty')]"
        self.proceed_to_checkout_button = "//*[@id='top-cart-btn-checkout']"

    # ---- Actions ----
    def enter_search_keyword(self, keyword):
        logger.info(f"Entering search keyword: {keyword}")
        box = self.page.locator(self.search_input)
        box.wait_for(state="visible", timeout=10000)
        box.fill(keyword)

    def click_search_button(self):
        logger.info("Clicking search button")
        btn = self.page.locator(self.search_button)
        try:
            btn.wait_for(state="visible", timeout=10000)
            btn.click()
            logger.info("Clicked Search button successfully")
        except Exception as e:
            logger.error(f"Failed to click Search button: {e}")
            raise

    def get_search_results_header_text(self):
        logger.info("Getting search results header text")
        header = self.page.locator(self.search_results_header)
        header.wait_for(state="visible", timeout=10000)
        return header.inner_text()

    def select_adrienne_trek_jacket(self):
        prod_link = self.page.locator(self.product_link)
        prod_link.wait_for(state="visible", timeout=10000)
        prod_link.click()

    def select_size_small(self):
        logger.info("Selecting size Small")
        swatch = self.page.locator(self.size_small)
        swatch.wait_for(state="visible", timeout=10000)
        swatch.click()

    def select_color_blue(self):
        logger.info("Selecting color Blue")
        color_opt = self.page.locator(self.color_blue)
        color_opt.wait_for(state="visible", timeout=10000)
        color_opt.click()

    def add_to_cart(self):
        logger.info("Clicking Add to Cart")
        btn = self.page.locator(self.add_to_cart_button)
        btn.wait_for(state="visible", timeout=10000)
        btn.click()

    def click_cart_icon(self):
        logger.info("Clicking cart icon (top right)")
        cart_btn = self.page.locator(self.cart_icon)
        cart_btn.wait_for(state="visible", timeout=10000)
        cart_btn.click()

    def click_proceed_to_checkout(self):
        logger.info("Clicking Proceed to Checkout button")
        self.page.locator("#minicart-content-wrapper").wait_for(state="visible", timeout=10000)
        checkout_btn = self.page.locator(self.proceed_to_checkout_button)
        checkout_btn.wait_for(state="visible", timeout=10000)
        checkout_btn.click()