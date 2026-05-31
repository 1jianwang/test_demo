"""
LoginPage - 登录页面对象

封装SauceDemo登录页面的元素定位和操作方法。
提供登录、获取错误消息等功能。
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """登录页面对象类"""

    # 页面元素定位器
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username, password):
        """
        执行登录操作

        Args:
            username: 用户名
            password: 密码

        Returns:
            self: 支持链式调用

        Example:
            LoginPage(driver).login("standard_user", "secret_sauce")
        """
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def error_message(self):
        """
        获取登录错误提示信息

        Returns:
            str: 错误消息文本

        Note:
            仅在登录失败时调用，否则会超时
        """
        return self.text_of(self.ERROR_MESSAGE)

