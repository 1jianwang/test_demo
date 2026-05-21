import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_011 商品列表页正常显示所有商品信息")
def test_商品列表正常显示(logged_in_driver):
    with allure.step("获取商品列表"):
        products = logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(products) > 0

    with allure.step("验证每个商品的完整信息"):
        for product in products:
            assert product.find_element(By.CLASS_NAME, "inventory_item_name").text != ""
            assert product.find_element(By.CLASS_NAME, "inventory_item_desc").text != ""
            assert product.find_element(By.CLASS_NAME, "inventory_item_price").text != ""
            assert product.find_element(By.TAG_NAME, "img").get_attribute("src") != ""
            assert product.find_element(By.TAG_NAME, "button").is_displayed()

@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_012 按名称A-Z排序")
def test_排序名称A到Z(logged_in_driver):
    with allure.step("点击排序下拉框"):
        logged_in_driver.find_element(By.CLASS_NAME, "product_sort_container").click()

    with allure.step("选择A-Z排序"):
        logged_in_driver.find_element(By.XPATH, "//option[@value='az']").click()

    with allure.step("等待排序完成并验证结果"):
        WebDriverWait(logged_in_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        names = [item.text for item in logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        assert names == sorted(names)

@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_013 按名称Z-A排序")
def test_排序名称Z到A(logged_in_driver):
    with allure.step("点击排序下拉框"):
        logged_in_driver.find_element(By.CLASS_NAME, "product_sort_container").click()

    with allure.step("选择Z-A排序"):
        logged_in_driver.find_element(By.XPATH, "//option[@value='za']").click()

    with allure.step("等待排序完成并验证结果"):
        WebDriverWait(logged_in_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        names = [item.text for item in logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        assert names == sorted(names, reverse=True)

@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_014 按价格从低到高排序")
def test_排序价格从低到高(logged_in_driver):
    with allure.step("点击排序下拉框"):
        logged_in_driver.find_element(By.CLASS_NAME, "product_sort_container").click()

    with allure.step("选择价格从低到高排序"):
        logged_in_driver.find_element(By.XPATH, "//option[@value='lohi']").click()

    with allure.step("等待排序完成并验证结果"):
        WebDriverWait(logged_in_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_price"))
        )
        prices = [float(item.text.replace("$", "")) for item in logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        assert prices == sorted(prices)

@allure.feature("商品模块")
@allure.story("排序功能")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_015 按价格从高到低排序")
def test_排序价格从高到低(logged_in_driver):
    with allure.step("点击排序下拉框"):
        logged_in_driver.find_element(By.CLASS_NAME, "product_sort_container").click()

    with allure.step("选择价格从高到低排序"):
        logged_in_driver.find_element(By.XPATH, "//option[@value='hilo']").click()

    with allure.step("等待排序完成并验证结果"):
        WebDriverWait(logged_in_driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_price"))
        )
        prices = [float(item.text.replace("$", "")) for item in logged_in_driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        assert prices == sorted(prices, reverse=True)

@allure.feature("商品模块")
@allure.story("购物车操作")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_016 点击购物车显示已加入的商品")
def test_购物车显示商品(logged_in_driver):
    wait = WebDriverWait(logged_in_driver, 10)

    with allure.step("点击加入购物车按钮"):
        logged_in_driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    with allure.step("点击购物车图标"):
        logged_in_driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    with allure.step("验证购物车中显示商品"):
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))
        items = logged_in_driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items) > 0
        for item in items:
            assert item.find_element(By.TAG_NAME, "button").is_displayed()

@allure.feature("商品模块")
@allure.story("购物车操作")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_017 点击remove移除商品购物车角标减1")
def test_移除购物车商品(logged_in_driver):
    wait = WebDriverWait(logged_in_driver, 10)

    with allure.step("点击加入购物车按钮"):
        logged_in_driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    with allure.step("点击购物车图标"):
        logged_in_driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

    with allure.step("等待移除按钮出现"):
        wait.until(EC.presence_of_element_located((By.ID, "remove-sauce-labs-backpack")))

    with allure.step("点击移除按钮"):
        logged_in_driver.find_element(By.ID, "remove-sauce-labs-backpack").click()

    with allure.step("验证购物车角标消失"):
        badges = logged_in_driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0

@allure.feature("商品模块")
@allure.story("商品列表")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC_018 点击商品跳转到详情页")
def test_点击商品进入详情页(logged_in_driver):
    wait = WebDriverWait(logged_in_driver, 10)

    with allure.step("点击商品名称"):
        logged_in_driver.find_element(By.CLASS_NAME, "inventory_item_name").click()

    with allure.step("验证跳转到详情页"):
        wait.until(EC.url_contains("inventory-item"))
        assert "inventory-item" in logged_in_driver.current_url

@allure.feature("商品模块")
@allure.story("购物车操作")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC_019 加入购物车后角标显示数字1")
def test_加入购物车角标显示(logged_in_driver):
    wait = WebDriverWait(logged_in_driver, 10)

    with allure.step("点击加入购物车按钮"):
        logged_in_driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    with allure.step("验证购物车角标显示数字1"):
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        badge = logged_in_driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        assert badge == "1"
