"""
ProductsPage - 商品列表页面对象

封装SauceDemo商品列表页面的元素定位和操作方法。
提供商品浏览、排序、加入购物车等功能。
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ProductsPage(BasePage):
    """商品列表页面对象类"""

    # 页面元素定位器
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
        """
        等待页面加载完成

        Returns:
            self: 支持链式调用
        """
        self.find(self.INVENTORY_LIST)
        return self

    def product_count(self):
        """
        获取页面上的商品数量

        Returns:
            int: 商品数量
        """
        return len(self.find_all(self.INVENTORY_ITEM))

    def products_have_required_information(self):
        """
        验证所有商品是否包含必要信息（名称、描述、价格、图片、按钮）

        Returns:
            bool: 所有商品信息完整返回True，否则返回False
        """
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
        """
        按指定方式排序商品

        Args:
            value: 排序方式
                - "az": 名称A到Z
                - "za": 名称Z到A
                - "lohi": 价格从低到高
                - "hilo": 价格从高到低

        Returns:
            self: 支持链式调用
        """
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def product_names(self):
        """
        获取所有商品名称列表

        Returns:
            list[str]: 商品名称列表
        """
        return self.texts_of(self.ITEM_NAME)

    def product_prices(self):
        """
        获取所有商品价格列表

        Returns:
            list[float]: 商品价格列表（已转换为浮点数）
        """
        return [float(price.replace("$", "")) for price in self.texts_of(self.ITEM_PRICE)]

    def add_backpack_to_cart(self):
        """
        将背包商品加入购物车

        Returns:
            self: 支持链式调用

        Note:
            添加后会等待0.5秒让DOM更新完成
        """
        self.click(self.BACKPACK_ADD_BUTTON)
        # 等待购物车角标出现（DOM更新需要时间）
        import time
        time.sleep(0.5)
        return self

    def remove_backpack_from_cart(self):
        """
        从购物车移除背包商品

        Returns:
            self: 支持链式调用
        """
        self.click(self.BACKPACK_REMOVE_BUTTON)
        return self

    def open_cart(self):
        """
        打开购物车页面

        Returns:
            self: 支持链式调用

        Note:
            优先使用href跳转，失败则使用JS点击
        """
        cart_url = self.find(self.CART_LINK).get_attribute("href")
        if cart_url:
            self.driver.get(cart_url)
        else:
            self.js_click(self.CART_LINK)
        self.wait_until_url_contains("cart")
        return self

    def cart_badge_text(self):
        """
        获取购物车角标文本

        Returns:
            str: 角标文本内容
        """
        return self.text_of(self.CART_BADGE)

    def cart_badge_count(self):
        """
        获取购物车角标上的商品数量

        Returns:
            int: 购物车中的商品数量，角标不存在时返回0

        Note:
            会等待0.5秒让DOM更新完成
        """
        import time
        time.sleep(0.5)  # 等待 DOM 更新
        elements = self.driver.find_elements(*self.CART_BADGE)
        if not elements:
            return 0
        try:
            badge_text = elements[0].text.strip()
            return int(badge_text) if badge_text else 0
        except (ValueError, AttributeError):
            return 0

    def open_first_product_detail(self):
        """
        打开第一个商品的详情页

        Returns:
            self: 支持链式调用
        """
        self.click(self.ITEM_NAME)
        return self

