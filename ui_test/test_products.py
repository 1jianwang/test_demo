import allure

from pages.cart_page import CartPage
from pages.products_page import ProductsPage


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_011 商品列表页正常显示所有商品信息")
def test_商品列表正常显示(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("获取商品列表"):
        assert products_page.product_count() > 0

    with allure.step("验证每个商品的完整信息"):
        assert products_page.products_have_required_information()


@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_012 按名称A-Z排序")
def test_排序名称A到Z(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("选择A-Z排序"):
        products_page.sort_by("az")

    with allure.step("验证排序结果"):
        names = products_page.product_names()
        assert names == sorted(names)


@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_013 按名称Z-A排序")
def test_排序名称Z到A(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("选择Z-A排序"):
        products_page.sort_by("za")

    with allure.step("验证排序结果"):
        names = products_page.product_names()
        assert names == sorted(names, reverse=True)


@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_014 按价格从低到高排序")
def test_排序价格从低到高(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("选择价格从低到高排序"):
        products_page.sort_by("lohi")

    with allure.step("验证排序结果"):
        prices = products_page.product_prices()
        assert prices == sorted(prices)


@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_015 按价格从高到低排序")
def test_排序价格从高到低(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("选择价格从高到低排序"):
        products_page.sort_by("hilo")

    with allure.step("验证排序结果"):
        prices = products_page.product_prices()
        assert prices == sorted(prices, reverse=True)


@allure.feature("商品模块")
@allure.story("购物车操作")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_016 点击购物车显示已加入的商品")
def test_购物车显示商品(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("加入商品并进入购物车"):
        products_page.add_backpack_to_cart().open_cart()

    with allure.step("验证购物车中显示商品"):
        cart_page = CartPage(logged_in_driver).wait_loaded()
        assert cart_page.item_count() > 0
        assert cart_page.items_have_action_buttons()


@allure.feature("商品模块")
@allure.story("购物车操作")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_017 点击remove移除商品购物车角标减1")
def test_移除购物车商品(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("加入商品并进入购物车"):
        products_page.add_backpack_to_cart().open_cart()

    with allure.step("移除购物车商品"):
        CartPage(logged_in_driver).wait_loaded().remove_backpack()

    with allure.step("验证购物车角标消失"):
        assert products_page.cart_badge_count() == 0


@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_018 点击商品跳转到详情页")
def test_点击商品进入详情页(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("点击商品名称"):
        products_page.open_first_product_detail()

    with allure.step("验证跳转到详情页"):
        products_page.wait_until_url_contains("inventory-item")
        assert "inventory-item" in logged_in_driver.current_url


@allure.feature("商品模块")
@allure.story("购物车操作")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_019 加入购物车后角标显示数字1")
def test_加入购物车角标显示(logged_in_driver):
    products_page = ProductsPage(logged_in_driver)

    with allure.step("点击加入购物车按钮"):
        products_page.add_backpack_to_cart()

    with allure.step("验证购物车角标显示数字1"):
        assert products_page.cart_badge_text() == "1"
