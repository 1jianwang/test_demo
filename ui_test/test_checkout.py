import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Checkout")
@allure.story("正常下单")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_020 正常下单全流程")
def test_正常下单(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("输入名字"):
        checkout_driver.find_element(By.ID, "first-name").send_keys("John")

    with allure.step("输入姓氏"):
        checkout_driver.find_element(By.ID, "last-name").send_keys("Doe")

    with allure.step("输入邮编"):
        checkout_driver.find_element(By.ID, "postal-code").send_keys("12345")

    with allure.step("点击Continue按钮"):
        checkout_driver.find_element(By.ID, "continue").click()

    with allure.step("等待进入订单确认页"):
        wait.until(EC.presence_of_element_located((By.ID, "finish")))

    with allure.step("点击Finish按钮"):
        checkout_driver.find_element(By.ID, "finish").click()

    with allure.step("验证订单完成提示"):
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
        title = checkout_driver.find_element(By.CLASS_NAME, "complete-header").text
        assert title == "Thank you for your order!"

@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_021 全部为空点击Continue")
def test_全部为空(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("不填写任何信息直接点击Continue"):
        checkout_driver.find_element(By.ID, "continue").click()

    with allure.step("验证错误提示"):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        error_msg = checkout_driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        assert error_msg == "Error: First Name is required"

@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_022 名字为空")
def test_名字为空(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("输入姓氏"):
        checkout_driver.find_element(By.ID, "last-name").send_keys("Doe")

    with allure.step("输入邮编"):
        checkout_driver.find_element(By.ID, "postal-code").send_keys("12345")

    with allure.step("点击Continue按钮"):
        checkout_driver.find_element(By.ID, "continue").click()

    with allure.step("验证错误提示"):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        error_msg = checkout_driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        assert error_msg == "Error: First Name is required"

@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_023 姓氏为空")
def test_姓氏为空(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("输入名字"):
        checkout_driver.find_element(By.ID, "first-name").send_keys("John")

    with allure.step("输入邮编"):
        checkout_driver.find_element(By.ID, "postal-code").send_keys("12345")

    with allure.step("点击Continue按钮"):
        checkout_driver.find_element(By.ID, "continue").click()

    with allure.step("验证错误提示"):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        error_msg = checkout_driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        assert error_msg == "Error: Last Name is required"

@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_024 邮编为空")
def test_邮编为空(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("输入名字"):
        checkout_driver.find_element(By.ID, "first-name").send_keys("John")

    with allure.step("输入姓氏"):
        checkout_driver.find_element(By.ID, "last-name").send_keys("Doe")

    with allure.step("点击Continue按钮"):
        checkout_driver.find_element(By.ID, "continue").click()

    with allure.step("验证错误提示"):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        error_msg = checkout_driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        assert error_msg == "Error: Postal Code is required"

@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_026 邮编填字母-系统未校验格式(Bug)")
def test_邮编填字母(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("输入名字"):
        checkout_driver.find_element(By.ID, "first-name").send_keys("John")

    with allure.step("输入姓氏"):
        checkout_driver.find_element(By.ID, "last-name").send_keys("Doe")

    with allure.step("输入字母邮编"):
        checkout_driver.find_element(By.ID, "postal-code").send_keys("abcde")

    with allure.step("点击Continue按钮"):
        checkout_driver.find_element(By.ID, "continue").click()

    with allure.step("验证进入订单确认页"):
        wait.until(EC.url_contains("checkout-step-two"))
        assert "checkout-step-two" in checkout_driver.current_url

@allure.feature("结算模块")
@allure.story("取消操作")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_027 点击Cancel返回购物车")
def test_取消下单(checkout_driver):
    wait = WebDriverWait(checkout_driver, 10)

    with allure.step("点击Cancel按钮"):
        checkout_driver.find_element(By.ID, "cancel").click()

    with allure.step("验证返回购物车页面"):
        wait.until(EC.url_contains("cart"))
        assert "cart" in checkout_driver.current_url
