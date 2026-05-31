"""登录功能UI测试模块"""

import allure

from pages.login_page import LoginPage


INVALID_CREDENTIAL_MESSAGE = "Epic sadface: Username and password do not match any user in this service"


@allure.feature("登录模块")
@allure.story("正常登录")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_001 正常登录-跳转商品页")
def test_正常登录(driver):
    """使用正确的用户名密码登录，验证跳转到商品页"""
    login_page = LoginPage(driver)

    with allure.step("输入用户名、密码并点击登录"):
        login_page.login("standard_user", "secret_sauce")

    with allure.step("等待页面跳转并验证URL"):
        login_page.wait_until_url_contains("inventory")
        assert "inventory" in driver.current_url


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_002 密码错误-提示用户名密码不匹配")
def test_密码错误(driver):
    """密码错误时显示错误提示"""
    login_page = LoginPage(driver)

    with allure.step("使用错误密码登录"):
        login_page.login("standard_user", "wrong_password")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == INVALID_CREDENTIAL_MESSAGE


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_003 用户名错误-提示用户名密码不匹配")
def test_用户名错误(driver):
    """用户名错误时显示错误提示"""
    login_page = LoginPage(driver)

    with allure.step("使用错误用户名登录"):
        login_page.login("wrong_user", "secret_sauce")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == INVALID_CREDENTIAL_MESSAGE


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_004 用户名密码都错-提示用户名密码不匹配")
def test_用户名密码都错(driver):
    """用户名和密码都错误时显示错误提示"""
    login_page = LoginPage(driver)

    with allure.step("使用错误用户名和错误密码登录"):
        login_page.login("wrong_user", "wrong_password")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == INVALID_CREDENTIAL_MESSAGE


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_005 用户名为空-提示用户名必填")
def test_用户名为空(driver):
    """用户名为空时显示必填提示"""
    login_page = LoginPage(driver)

    with allure.step("用户名为空时点击登录"):
        login_page.login("", "secret_sauce")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == "Epic sadface: Username is required"


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_006 密码为空-提示密码必填")
def test_密码为空(driver):
    """密码为空时显示必填提示"""
    login_page = LoginPage(driver)

    with allure.step("密码为空时点击登录"):
        login_page.login("standard_user", "")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == "Epic sadface: Password is required"


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_007 用户名密码都为空-提示用户名必填")
def test_用户名密码都为空(driver):
    """用户名和密码都为空时显示用户名必填提示"""
    login_page = LoginPage(driver)

    with allure.step("用户名和密码都为空时点击登录"):
        login_page.login("", "")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == "Epic sadface: Username is required"


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_008 超长用户名-登录失败系统不崩溃")
def test_超长用户名(driver):
    """输入300字符超长用户名，验证系统不崩溃"""
    login_page = LoginPage(driver)

    with allure.step("输入超长用户名并登录"):
        login_page.login("a" * 300, "secret_sauce")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == INVALID_CREDENTIAL_MESSAGE


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_009 特殊字符用户名-登录失败脚本未执行")
def test_特殊字符用户名(driver):
    """输入包含脚本的用户名，验证系统防XSS攻击"""
    login_page = LoginPage(driver)

    with allure.step("输入特殊字符用户名并登录"):
        login_page.login("<script>alert(1)</script>", "secret_sauce")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == INVALID_CREDENTIAL_MESSAGE


@allure.feature("登录模块")
@allure.story("异常登录")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_010 封禁账号-提示账号已锁定")
def test_封禁账号(driver):
    """使用封禁账号登录，验证显示锁定提示"""
    login_page = LoginPage(driver)

    with allure.step("使用封禁账号登录"):
        login_page.login("locked_out_user", "secret_sauce")

    with allure.step("验证错误提示"):
        assert login_page.error_message() == "Epic sadface: Sorry, this user has been locked out."
