import os
import platform

import allure
import pytest
import requests
from requests.adapters import HTTPAdapter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from urllib3.util.retry import Retry

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


BASE_API_URL = os.getenv("BASE_API_URL", "https://jsonplaceholder.typicode.com")
BASE_UI_URL = os.getenv("BASE_UI_URL", "https://www.saucedemo.com")
HEADLESS = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}
CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")


class ApiSession(requests.Session):
    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", 10)
        return super().request(method, url, **kwargs)


def pytest_configure(config):
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"Browser=Chrome\n")
        f.write(f"Base.UI.URL={BASE_UI_URL}\n")
        f.write(f"Base.API.URL={BASE_API_URL}\n")
        f.write(f"Headless={HEADLESS}\n")
        f.write(f"Chrome.Driver.Path={CHROME_DRIVER_PATH or 'Selenium Manager'}\n")
        f.write(f"Environment=Test\n")
        f.write(f"Python.Version={platform.python_version()}\n")


@pytest.fixture
def api():
    session = ApiSession()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = BASE_API_URL
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods={"GET", "POST", "PUT", "DELETE"},
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    yield session
    session.close()


@pytest.fixture
def driver():
    options = Options()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        if CHROME_DRIVER_PATH:
            d = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
        else:
            d = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        pytest.skip(f"Chrome WebDriver is not available in this environment: {exc.msg}")

    d.get(BASE_UI_URL)
    yield d
    d.quit()


@pytest.fixture
def logged_in_driver(driver):
    LoginPage(driver).login("standard_user", "secret_sauce")
    ProductsPage(driver).wait_loaded()
    yield driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
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
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass


@pytest.fixture
def checkout_driver(logged_in_driver):
    ProductsPage(logged_in_driver).add_backpack_to_cart().open_cart()
    CartPage(logged_in_driver).wait_loaded().checkout()
    CheckoutPage(logged_in_driver).wait_loaded()
    yield logged_in_driver
