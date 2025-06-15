from datetime import *
import random
qa_url = "https://www.amazon.in/"


class HomePage:
    Url = "https://www.amazon.in/"
    Logo = "id=nav-logo-sprites"
    Searchbox = "id=twotabsearchtextbox"
    Searchbutton = "id=nav-search-submit-button"
    Firstresult = "(//h2[contains(@class, 'a-size-medium') and contains(@class, 'a-text-normal')]//span)"
    Addtocart = "text=Add to Cart"
    Gotocart = "id=nav-cart-count"
    Viewcart = "//div[@id='nav-cart-count-container']"
    Cartitemradiobutton = "//input[@type='checkbox']/ancestor::div[@class='a-checkbox a-checkbox-fancy sc-item-check-checkbox-selector sc-list-item-checkbox']"
    Saveforlater = "//input[@value='Save for later']"
    Movetocart = "(//input[@data-action='move-to-cart']/ancestor::span[@class='a-button-inner'])[1]"
    incrementicon = "//span[@class ='a-icon a-icon-small-add']"
    decrementicon = "//span[@class ='a-icon a-icon-small-remove']"
    Delete = "//input[@value='Delete']"
