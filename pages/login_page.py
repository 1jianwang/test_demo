"""登录页面对象"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):

    # 页面元素定位器
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def login(self, username, password):
        """执行登录操作"""
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def error_message(self):
        """获取登录错误提示信息"""
        return self.text_of(self.ERROR_MESSAGE)

