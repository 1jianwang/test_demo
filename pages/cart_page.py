from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BACKPACK_BUTTON = (By.ID, "remove-sauce-labs-backpack")

    def wait_loaded(self):
        self.find(self.CART_LIST)
        return self

    def item_count(self):
        return len(self.find_all(self.CART_ITEM))

    def items_have_action_buttons(self):
        return all(item.find_element(By.TAG_NAME, "button").is_displayed() for item in self.find_all(self.CART_ITEM))

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK_BUTTON)
        return self

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self
