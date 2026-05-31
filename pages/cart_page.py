"""购物车页面对象"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):

    # 页面元素定位器
    CART_LIST = (By.CSS_SELECTOR, "[data-test='cart-list'], .cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BACKPACK_BUTTON = (By.ID, "remove-sauce-labs-backpack")

    def wait_loaded(self):
        """等待购物车页面加载完成"""
        self.wait_until_url_contains("cart")
        self.find(self.CART_LIST)
        self.find(self.CHECKOUT_BUTTON)
        return self

    def item_count(self):
        """获取购物车中的商品数量"""
        elements = self.driver.find_elements(*self.CART_ITEM)
        return len(elements)

    def items_have_action_buttons(self):
        """检查所有商品是否都有操作按钮"""
        return all(item.find_element(By.TAG_NAME, "button").is_displayed() for item in self.find_all(self.CART_ITEM))

    def remove_backpack(self):
        """从购物车移除背包商品"""
        self.click(self.REMOVE_BACKPACK_BUTTON)
        import time
        time.sleep(0.5)
        return self

    def checkout(self):
        """点击结算按钮，进入结算流程"""
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_until_url_contains("checkout-step-one")
        return self

