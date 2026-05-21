import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("登录模块")
@allure.story("正常登录")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_001 正常登录-跳转商品页")
def test_正常登录(driver):
    with allure.step("输入用户名"):
        driver.find_element(By.ID, "user-name").send_keys("standard_user")

    with allure.step("输入密码"):
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("等待页面跳转并验证URL"):
        WebDriverWait(driver, 10).until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_002 密码错误-提示用户名密码不匹配")
def test_密码错误(driver):
    with allure.step("输入用户名"):
        driver.find_element(By.ID, "user-name").send_keys("standard_user")

    with allure.step("输入错误密码"):
        driver.find_element(By.ID, "password").send_keys("wrong_password")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username and password do not match any user in this service"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_003 用户名错误-提示用户名密码不匹配")
def test_用户名错误(driver):
    with allure.step("输入错误用户名"):
        driver.find_element(By.ID, "user-name").send_keys("wrong_user")

    with allure.step("输入密码"):
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username and password do not match any user in this service"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_004 用户名密码都错-提示用户名密码不匹配")
def test_用户名密码都错(driver):
    with allure.step("输入错误用户名"):
        driver.find_element(By.ID, "user-name").send_keys("wrong_user")

    with allure.step("输入错误密码"):
        driver.find_element(By.ID, "password").send_keys("wrong_password")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username and password do not match any user in this service"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_005 用户名为空-提示用户名必填")
def test_用户名为空(driver):
    with allure.step("输入空用户名"):
        driver.find_element(By.ID, "user-name").send_keys("")

    with allure.step("输入密码"):
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username is required"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_006 密码为空-提示密码必填")
def test_密码为空(driver):
    with allure.step("输入用户名"):
        driver.find_element(By.ID, "user-name").send_keys("standard_user")

    with allure.step("输入空密码"):
        driver.find_element(By.ID, "password").send_keys("")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Password is required"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_007 用户名密码都为空-提示用户名必填")
def test_用户名密码都为空(driver):
    with allure.step("输入空用户名"):
        driver.find_element(By.ID, "user-name").send_keys("")

    with allure.step("输入空密码"):
        driver.find_element(By.ID, "password").send_keys("")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username is required"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_008 超长用户名-登录失败系统不崩溃")
def test_超长用户名(driver):
    with allure.step("输入超长用户名"):
        driver.find_element(By.ID, "user-name").send_keys("a" * 300)

    with allure.step("输入密码"):
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username and password do not match any user in this service"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_009 特殊字符用户名-登录失败脚本未执行")
def test_特殊字符用户名(driver):
    with allure.step("输入特殊字符用户名"):
        driver.find_element(By.ID, "user-name").send_keys("<script>alert(1)</script>")

    with allure.step("输入密码"):
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Username and password do not match any user in this service"

@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_010 封禁账号-提示账号已锁定")
def test_封禁账号(driver):
    with allure.step("输入封禁账号用户名"):
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")

    with allure.step("输入密码"):
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("点击登录按钮"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("验证错误提示"):
        error_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        error_msg = error_element.text
        assert error_msg == "Epic sadface: Sorry, this user has been locked out."
