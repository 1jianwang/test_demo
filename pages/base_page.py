"""页面对象基类，封装常用的Selenium操作方法"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """页面对象基类"""

    def __init__(self, driver, timeout=20):
        """初始化页面对象"""
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        """打开指定URL"""
        self.driver.get(url)
        return self

    def find(self, locator):
        """查找单个元素"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """查找多个元素"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """点击元素"""
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def js_click(self, locator):
        """使用JavaScript点击元素"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def type_text(self, locator, text, clear=True):
        """在输入框中输入文本"""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        if text:
            element.send_keys(text)
        return self

    def text_of(self, locator):
        """获取元素的文本内容"""
        return self.find(locator).text

    def texts_of(self, locator):
        """获取多个元素的文本内容列表"""
        return [element.text for element in self.find_all(locator)]

    def exists(self, locator):
        """检查元素是否存在"""
        return len(self.driver.find_elements(*locator)) > 0

    def wait_until_url_contains(self, value):
        """等待URL包含指定字符串"""
        self.wait.until(EC.url_contains(value))
        return self

