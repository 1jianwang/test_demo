from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ProductsPage(BasePage):
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_DESCRIPTION = (By.CLASS_NAME, "inventory_item_desc")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    BACKPACK_REMOVE_BUTTON = (By.ID, "remove-sauce-labs-backpack")

    def wait_loaded(self):
        self.find(self.INVENTORY_LIST)
        return self

    def product_count(self):
        return len(self.find_all(self.INVENTORY_ITEM))

    def products_have_required_information(self):
        for product in self.find_all(self.INVENTORY_ITEM):
            if product.find_element(*self.ITEM_NAME).text == "":
                return False
            if product.find_element(*self.ITEM_DESCRIPTION).text == "":
                return False
            if product.find_element(*self.ITEM_PRICE).text == "":
                return False
            if product.find_element(By.TAG_NAME, "img").get_attribute("src") == "":
                return False
            if not product.find_element(By.TAG_NAME, "button").is_displayed():
                return False
        return True

    def sort_by(self, value):
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def product_names(self):
        return self.texts_of(self.ITEM_NAME)

    def product_prices(self):
        return [float(price.replace("$", "")) for price in self.texts_of(self.ITEM_PRICE)]

    def add_backpack_to_cart(self):
        self.click(self.BACKPACK_ADD_BUTTON)
        self.find(self.CART_BADGE)
        return self

    def remove_backpack_from_cart(self):
        self.click(self.BACKPACK_REMOVE_BUTTON)
        return self

    def open_cart(self):
        cart_url = self.find(self.CART_LINK).get_attribute("href")
        if cart_url:
            self.driver.get(cart_url)
        else:
            self.js_click(self.CART_LINK)
        self.wait_until_url_contains("cart")
        return self

    def cart_badge_text(self):
        return self.text_of(self.CART_BADGE)

    def cart_badge_count(self):
        """返回购物车角标上的数字，如果角标不存在则返回 0"""
        elements = self.driver.find_elements(*self.CART_BADGE)
        if elements:
            try:
                return int(elements[0].text)
            except (ValueError, AttributeError):
                return 0
        return 0

    def open_first_product_detail(self):
        self.click(self.ITEM_NAME)
        return self
