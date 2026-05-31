from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CSS_SELECTOR, "[data-test='cart-list'], .cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BACKPACK_BUTTON = (By.ID, "remove-sauce-labs-backpack")

    def wait_loaded(self):
        self.wait_until_url_contains("cart")
        self.find(self.CART_LIST)
        self.find(self.CHECKOUT_BUTTON)
        return self

    def item_count(self):
        return len(self.find_all(self.CART_ITEM))

    def items_have_action_buttons(self):
        return all(item.find_element(By.TAG_NAME, "button").is_displayed() for item in self.find_all(self.CART_ITEM))

    def remove_backpack(self):
        self.click(self.REMOVE_BACKPACK_BUTTON)
        # 等待购物车角标更新或消失
        from selenium.webdriver.common.by import By
        import time
        time.sleep(0.5)  # 给 DOM 更新时间
        return self

    def checkout(self):
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_until_url_contains("checkout-step-one")
        return self
