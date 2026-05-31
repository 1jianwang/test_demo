"""
CheckoutPage - 结算页面对象

封装SauceDemo结算页面的元素定位和操作方法。
包含两个步骤：step-one（填写收货信息）和step-two（确认订单）。
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """结算页面对象类"""

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
        """
        等待结算页面（step-one）加载完成

        Returns:
            self: 支持链式调用
        """
        self.wait_until_url_contains("checkout-step-one")
        self.find(self.FIRST_NAME_INPUT)
        return self

    def fill_customer_info(self, first_name="", last_name="", postal_code=""):
        """
        填写收货信息

        Args:
            first_name: 名字，默认为空字符串
            last_name: 姓氏，默认为空字符串
            postal_code: 邮政编码，默认为空字符串

        Returns:
            self: 支持链式调用

        Note:
            空字符串用于测试表单验证场景
        """
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_checkout(self):
        """
        点击Continue按钮，进入下一步

        Returns:
            self: 支持链式调用

        Note:
            点击后会等待0.5秒，让页面有时间响应（跳转或显示错误）
        """
        self.click(self.CONTINUE_BUTTON)
        # 等待页面跳转或停留（如果有验证错误）
        import time
        time.sleep(0.5)  # 给页面响应时间
        return self

    def cancel(self):
        """
        点击Cancel按钮，取消结算

        Returns:
            self: 支持链式调用

        Note:
            使用JS点击并等待页面跳转到cart页面
        """
        self.js_click(self.CANCEL_BUTTON)
        self.wait_until_url_contains("cart")
        return self

    def finish(self):
        """
        完成订单（在step-two页面点击Finish按钮）

        Returns:
            self: 支持链式调用

        Note:
            会先等待进入checkout-step-two页面，再点击Finish按钮，
            最后等待完成页面的URL和标题元素出现
        """
        # 等待进入 step-two 页面
        self.wait_until_url_contains("checkout-step-two")
        self.click(self.FINISH_BUTTON)
        # 等待跳转到完成页面
        self.wait_until_url_contains("checkout-complete")
        # 等待完成页面的标题元素出现
        self.find(self.COMPLETE_HEADER)
        return self

    def error_message(self):
        """
        获取表单验证错误消息

        Returns:
            str: 错误消息文本

        Note:
            仅在表单验证失败时调用，否则会超时
        """
        return self.text_of(self.ERROR_MESSAGE)

    def complete_message(self):
        """
        获取订单完成提示消息

        Returns:
            str: 完成消息文本（通常为"Thank you for your order!"）
        """
        return self.text_of(self.COMPLETE_HEADER)

