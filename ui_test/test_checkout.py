import allure

from pages.checkout_page import CheckoutPage


@allure.feature("结算模块")
@allure.story("正常下单")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_020 正常下单全流程")
def test_正常下单(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("填写收货信息"):
        checkout_page.fill_customer_info("John", "Doe", "12345")

    with allure.step("进入订单确认页"):
        checkout_page.continue_checkout()

    with allure.step("提交订单"):
        checkout_page.finish()

    with allure.step("验证订单完成提示"):
        assert checkout_page.complete_message() == "Thank you for your order!"


@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_021 全部为空点击Continue")
def test_全部为空(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("不填写任何信息直接点击Continue"):
        checkout_page.continue_checkout()

    with allure.step("验证错误提示"):
        assert checkout_page.error_message() == "Error: First Name is required"


@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_022 名字为空")
def test_名字为空(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("只填写姓氏和邮编"):
        checkout_page.fill_customer_info("", "Doe", "12345").continue_checkout()

    with allure.step("验证错误提示"):
        assert checkout_page.error_message() == "Error: First Name is required"


@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_023 姓氏为空")
def test_姓氏为空(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("只填写名字和邮编"):
        checkout_page.fill_customer_info("John", "", "12345").continue_checkout()

    with allure.step("验证错误提示"):
        assert checkout_page.error_message() == "Error: Last Name is required"


@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_024 邮编为空")
def test_邮编为空(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("只填写名字和姓氏"):
        checkout_page.fill_customer_info("John", "Doe", "").continue_checkout()

    with allure.step("验证错误提示"):
        assert checkout_page.error_message() == "Error: Postal Code is required"


@allure.feature("结算模块")
@allure.story("表单校验")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_026 邮编填字母-系统未校验格式(Bug)")
def test_邮编填字母(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("输入字母邮编"):
        checkout_page.fill_customer_info("John", "Doe", "abcde").continue_checkout()

    with allure.step("验证进入订单确认页"):
        checkout_page.wait_until_url_contains("checkout-step-two")
        assert "checkout-step-two" in checkout_driver.current_url


@allure.feature("结算模块")
@allure.story("取消操作")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC_027 点击Cancel返回购物车")
def test_取消下单(checkout_driver):
    checkout_page = CheckoutPage(checkout_driver)

    with allure.step("点击Cancel按钮"):
        checkout_page.cancel()

    with allure.step("验证返回购物车页面"):
        checkout_page.wait_until_url_contains("cart")
        assert "cart" in checkout_driver.current_url
