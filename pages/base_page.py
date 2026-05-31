from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Common Selenium operations shared by all Page Objects."""

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        return self

    def js_click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def type_text(self, locator, text, clear=True):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(text)
        return self

    def text_of(self, locator):
        return self.find(locator).text

    def texts_of(self, locator):
        return [element.text for element in self.find_all(locator)]

    def exists(self, locator):
        return len(self.driver.find_elements(*locator)) > 0

    def wait_until_url_contains(self, value):
        self.wait.until(EC.url_contains(value))
        return self
