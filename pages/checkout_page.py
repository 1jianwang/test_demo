from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def wait_loaded(self):
        self.find(self.FIRST_NAME_INPUT)
        return self

    def fill_customer_info(self, first_name="", last_name="", postal_code=""):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
        return self

    def finish(self):
        self.click(self.FINISH_BUTTON)
        return self

    def error_message(self):
        return self.text_of(self.ERROR_MESSAGE)

    def complete_message(self):
        return self.text_of(self.COMPLETE_HEADER)
