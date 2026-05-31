"""商品列表页面对象"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class ProductsPage(BasePage):

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
        """等待页面加载完成"""
        self.find(self.INVENTORY_LIST)
        return self

    def product_count(self):
        """获取页面上的商品数量"""
        return len(self.find_all(self.INVENTORY_ITEM))

    def products_have_required_information(self):
        """验证所有商品是否包含必要信息（名称、描述、价格、图片、按钮）"""
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
        """按指定方式排序商品"""
        Select(self.find(self.SORT_SELECT)).select_by_value(value)
        return self

    def product_names(self):
        """获取所有商品名称列表"""
        return self.texts_of(self.ITEM_NAME)

    def product_prices(self):
        """获取所有商品价格列表"""
        return [float(price.replace("$", "")) for price in self.texts_of(self.ITEM_PRICE)]

    def add_backpack_to_cart(self):
        """将背包商品加入购物车"""
        self.click(self.BACKPACK_ADD_BUTTON)
        # 等待购物车徽章出现，确认商品已添加
        self.find(self.CART_BADGE)
        return self

    def remove_backpack_from_cart(self):
        """从购物车移除背包商品"""
        self.click(self.BACKPACK_REMOVE_BUTTON)
        return self

    def open_cart(self):
        """打开购物车页面"""
        cart_url = self.find(self.CART_LINK).get_attribute("href")
        if cart_url:
            self.driver.get(cart_url)
        else:
            self.js_click(self.CART_LINK)
        self.wait_until_url_contains("cart")
        return self

    def cart_badge_text(self):
        """获取购物车角标文本"""
        return self.text_of(self.CART_BADGE)

    def cart_badge_count(self):
        """获取购物车角标上的商品数量"""
        import time
        time.sleep(0.5)
        elements = self.driver.find_elements(*self.CART_BADGE)
        if not elements:
            return 0
        try:
            badge_text = elements[0].text.strip()
            return int(badge_text) if badge_text else 0
        except (ValueError, AttributeError):
            return 0

    def open_first_product_detail(self):
        """打开第一个商品的详情页"""
        self.click(self.ITEM_NAME)
        return self

