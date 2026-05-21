import pytest
import allure
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, platform

#自动配置environment.properties 文件，供allure报告使用
def pytest_configure(config):
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as f:
        f.write(f"Browser=Chrome\n")
        f.write(f"Base.URL=https://www.saucedemo.com\n")
        f.write(f"API.URL=https://jsonplaceholder.typicode.com\n")
        f.write(f"Environment=Test\n")
        f.write(f"Python.Version={platform.python_version()}\n")
# 常量定义
BASE_URL = "https://jsonplaceholder.typicode.com"
UI_URL = "https://www.saucedemo.com"

@pytest.fixture
def api():
    """接口测试 fixture：创建 requests.Session"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json"
    })
    session.base_url = BASE_URL
    yield session
    session.close()

@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    # 云端 CI 环境
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    d = webdriver.Chrome(options=options)
    d.get(UI_URL)
    yield d
    d.quit()

@pytest.fixture
def logged_in_driver(driver):
    """已登录 fixture：完成登录操作"""
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
    yield driver

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """失败自动截图 hook"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 尝试从 funcargs 中获取 driver 或 logged_in_driver
        driver_fixture = None
        if "driver" in item.funcargs:
            driver_fixture = item.funcargs["driver"]
        elif "logged_in_driver" in item.funcargs:
            driver_fixture = item.funcargs["logged_in_driver"]
        elif "checkout_driver" in item.funcargs:
            driver_fixture = item.funcargs["checkout_driver"]

        if driver_fixture:
            try:
                allure.attach(
                    driver_fixture.get_screenshot_as_png(),
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass
