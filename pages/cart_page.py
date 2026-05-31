"""
CartPage - 购物车页面对象

封装SauceDemo购物车页面的元素定位和操作方法。
提供查看购物车商品、移除商品、结算等功能。
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """购物车页面对象类"""

    # 页面元素定位器
    CART_LIST = (By.CSS_SELECTOR, "[data-test='cart-list'], .cart_list")
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BACKPACK_BUTTON = (By.ID, "remove-sauce-labs-backpack")

    def wait_loaded(self):
        """
        等待购物车页面加载完成

        Returns:
            self: 支持链式调用
        """
        self.wait_until_url_contains("cart")
        self.find(self.CART_LIST)
        self.find(self.CHECKOUT_BUTTON)
        return self

    def item_count(self):
        """
        获取购物车中的商品数量

        Returns:
            int: 商品数量，购物车为空时返回0

        Note:
            使用find_elements而非find_all，避免空购物车时超时
        """
        elements = self.driver.find_elements(*self.CART_ITEM)
        return len(elements)

    def items_have_action_buttons(self):
        """
        检查所有商品是否都有操作按钮

        Returns:
            bool: 所有商品都有按钮返回True，否则返回False
        """
        return all(item.find_element(By.TAG_NAME, "button").is_displayed() for item in self.find_all(self.CART_ITEM))

    def remove_backpack(self):
        """
        从购物车移除背包商品

        Returns:
            self: 支持链式调用

        Note:
            移除后会等待0.5秒让DOM更新完成
        """
        self.click(self.REMOVE_BACKPACK_BUTTON)
        # 等待购物车角标更新或消失
        import time
        time.sleep(0.5)  # 给 DOM 更新时间
        return self

    def checkout(self):
        """
        点击结算按钮，进入结算流程

        Returns:
            self: 支持链式调用

        Note:
            使用JS点击避免元素被遮挡，并等待跳转到checkout-step-one页面
        """
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_until_url_contains("checkout-step-one")
        return self

