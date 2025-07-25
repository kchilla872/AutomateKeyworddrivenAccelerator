from locators import HomePage


def go_to_homepage(page):
    page.goto(HomePage.Url)


def check_logo(page):
    assert page.locator(HomePage.Logo).is_visible()
    assert "Amazon" in page.title()


def search_item(page, item_name):
    page.fill(HomePage.Searchbox, item_name)
    page.click(HomePage.Searchbutton)
    page.wait_for_timeout(3000)


def add_first_search_result_to_cart(page):
    page.wait_for_selector(HomePage.Firstresult).click()
    page.wait_for_selector(HomePage.Addtocart).click()
    page.wait_for_timeout(4000)
    # Close popup if exists
    try:
        page.wait_for_selector(HomePage.PopupCloseButton, state="visible", timeout=5000)
        page.click(HomePage.PopupCloseButton)
    except:
        pass


def go_to_cart(page):
    page.wait_for_selector(HomePage.Gotocart).click()
    page.wait_for_timeout(3000)


def view_cart(page):
    assert page.wait_for_selector(HomePage.Viewcart).is_visible()
    page.click(HomePage.Viewcart)
    page.wait_for_timeout(1000)


def toggle_cart_item_checkbox(page):
    page.wait_for_selector(HomePage.Cartitemradiobutton).click()
    page.wait_for_timeout(1000)
    page.wait_for_selector(HomePage.Cartitemradiobutton).click()


def save_for_later(page):
    page.wait_for_selector(HomePage.Saveforlater, state="visible", timeout=10000)
    page.click(HomePage.Saveforlater)


def move_to_cart(page):
    page.wait_for_selector(HomePage.Movetocart).click()
    page.wait_for_timeout(1000)


def increment_item(page):
    page.wait_for_selector(HomePage.incrementicon).click()
    page.wait_for_timeout(60000)


def decrement_item(page):
    page.wait_for_selector(HomePage.decrementicon).click()
    page.wait_for_timeout(60000)


def delete_item(page):
    page.wait_for_selector(HomePage.Cartitemradiobutton).click()
    page.click(HomePage.Delete, timeout=60000)
