"""
BasePage - 页面对象基类

提供所有页面对象共享的通用Selenium操作方法，遵循Page Object Model (POM) 设计模式。
所有具体页面类都应继承此基类以复用常用的元素操作方法。
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """页面对象基类，封装常用的Selenium操作"""

    def __init__(self, driver, timeout=20):
        """
        初始化页面对象

        Args:
            driver: Selenium WebDriver实例
            timeout: 元素等待超时时间（秒），默认20秒
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        """
        打开指定URL

        Args:
            url: 要访问的网页地址

        Returns:
            self: 支持链式调用
        """
        self.driver.get(url)
        return self

    def find(self, locator):
        """
        查找单个元素（等待元素出现在DOM中）

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            WebElement: 找到的元素对象

        Raises:
            TimeoutException: 超时未找到元素
        """
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """
        查找多个元素（等待至少一个元素出现）

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            list[WebElement]: 找到的元素列表

        Raises:
            TimeoutException: 超时未找到任何元素
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """
        点击元素（等待元素可点击）

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            self: 支持链式调用

        Raises:
            TimeoutException: 超时未找到可点击元素
        """
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def js_click(self, locator):
        """
        使用JavaScript点击元素（用于处理被遮挡或不可见的元素）

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            self: 支持链式调用

        Note:
            当普通click()方法失败时使用此方法
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def type_text(self, locator, text, clear=True):
        """
        在输入框中输入文本

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")
            text: 要输入的文本内容
            clear: 是否先清空输入框，默认True

        Returns:
            self: 支持链式调用

        Note:
            只有当text不为空时才会执行输入操作
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        if text:  # 只有当 text 不为空时才输入
            element.send_keys(text)
        return self

    def text_of(self, locator):
        """
        获取元素的文本内容

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            str: 元素的文本内容
        """
        return self.find(locator).text

    def texts_of(self, locator):
        """
        获取多个元素的文本内容列表

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            list[str]: 所有匹配元素的文本内容列表
        """
        return [element.text for element in self.find_all(locator)]

    def exists(self, locator):
        """
        检查元素是否存在（不等待，立即返回）

        Args:
            locator: 元素定位器，格式为 (By.XXX, "value")

        Returns:
            bool: 元素存在返回True，否则返回False

        Note:
            此方法不会等待元素出现，适用于快速检查
        """
        return len(self.driver.find_elements(*locator)) > 0

    def wait_until_url_contains(self, value):
        """
        等待URL包含指定字符串

        Args:
            value: URL中应包含的字符串

        Returns:
            self: 支持链式调用

        Raises:
            TimeoutException: 超时URL仍不包含指定字符串

        Note:
            常用于验证页面跳转是否成功
        """
        self.wait.until(EC.url_contains(value))
        return self

