"""结算页面对象"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):

    # 页面元素定位器
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def wait_loaded(self):
        """等待结算页面加载完成"""
        self.wait_until_url_contains("checkout-step-one")
        self.find(self.FIRST_NAME_INPUT)
        return self

    def fill_customer_info(self, first_name="", last_name="", postal_code=""):
        """填写收货信息"""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_checkout(self):
        """点击Continue按钮，进入下一步"""
        self.click(self.CONTINUE_BUTTON)
        import time
        time.sleep(0.5)
        return self

    def cancel(self):
        """点击Cancel按钮，取消结算"""
        self.click(self.CANCEL_BUTTON)
        import time
        time.sleep(1)
        return self

    def finish(self):
        """完成订单"""
        self.wait_until_url_contains("checkout-step-two")
        self.click(self.FINISH_BUTTON)
        return self

    def error_message(self):
        """获取表单验证错误消息"""
        return self.text_of(self.ERROR_MESSAGE)

    def complete_message(self):
        """获取订单完成提示消息"""
        return self.text_of(self.COMPLETE_HEADER)

