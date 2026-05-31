"""
Pytest全局配置文件

提供测试所需的fixture和钩子函数，包括：
- 环境配置：从环境变量读取测试配置
- API测试：带重试机制的HTTP会话
- UI测试：WebDriver配置和页面对象fixture
- 测试报告：Allure报告集成和失败截图
"""

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


# ==================== 环境配置 ====================
# 从环境变量读取配置，提供默认值

BASE_API_URL = os.getenv("BASE_API_URL", "https://jsonplaceholder.typicode.com")
"""API测试基础URL"""

BASE_UI_URL = os.getenv("BASE_UI_URL", "https://www.saucedemo.com")
"""UI测试基础URL"""

HEADLESS = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}
"""是否使用无头模式运行浏览器"""

CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH")
"""ChromeDriver路径，为None时使用Selenium Manager自动管理"""


# ==================== API会话类 ====================

class ApiSession(requests.Session):
    """
    自定义API会话类，继承自requests.Session

    特性：
    - 自动设置10秒超时
    - 支持重试机制（通过HTTPAdapter配置）
    """

    def request(self, method, url, **kwargs):
        """
        重写request方法，为所有请求添加默认超时

        Args:
            method: HTTP方法（GET, POST等）
            url: 请求URL
            **kwargs: 其他请求参数

        Returns:
            Response: HTTP响应对象
        """
        kwargs.setdefault("timeout", 10)
        return super().request(method, url, **kwargs)


# ==================== Pytest钩子函数 ====================

def pytest_configure(config):
    """
    Pytest配置钩子，在测试运行前执行

    功能：
    - 创建allure-results目录
    - 生成environment.properties文件，记录测试环境信息

    Args:
        config: Pytest配置对象
    """
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"Browser=Chrome\n")
        f.write(f"Base.UI.URL={BASE_UI_URL}\n")
        f.write(f"Base.API.URL={BASE_API_URL}\n")
        f.write(f"Headless={HEADLESS}\n")
        f.write(f"Chrome.Driver.Path={CHROME_DRIVER_PATH or 'Selenium Manager'}\n")
        f.write(f"Environment=Test\n")
        f.write(f"Python.Version={platform.python_version()}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试报告生成钩子，在测试失败时自动截图

    功能：
    - 检测测试是否失败
    - 如果失败且有driver fixture，自动截图并附加到Allure报告

    Args:
        item: 测试项
        call: 测试调用信息

    Yields:
        测试结果
    """
    outcome = yield
    report = outcome.get_result()

    # 只在测试执行阶段（call）且失败时截图
    if report.when == "call" and report.failed:
        driver_fixture = None

        # 查找可用的driver fixture
        if "driver" in item.funcargs:
            driver_fixture = item.funcargs["driver"]
        elif "logged_in_driver" in item.funcargs:
            driver_fixture = item.funcargs["logged_in_driver"]
        elif "checkout_driver" in item.funcargs:
            driver_fixture = item.funcargs["checkout_driver"]

        # 如果找到driver，尝试截图
        if driver_fixture:
            try:
                allure.attach(
                    driver_fixture.get_screenshot_as_png(),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                # 截图失败时静默处理，不影响测试结果
                pass


# ==================== Fixture定义 ====================

@pytest.fixture
def api():
    """
    API测试会话fixture

    提供：
    - 自定义ApiSession实例
    - 自动设置Content-Type为application/json
    - 配置重试机制：最多重试3次，针对特定HTTP状态码
    - 指数退避策略：0.5秒基础延迟

    重试条件：
    - 连接错误：最多3次
    - 读取错误：最多3次
    - HTTP状态码：429, 500, 502, 503, 504
    - 允许的方法：GET, POST, PUT, DELETE

    Yields:
        ApiSession: 配置好的API会话对象

    清理：
        测试结束后自动关闭会话
    """
    session = ApiSession()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = BASE_API_URL

    # 配置重试策略
    retry = Retry(
        total=3,  # 总重试次数
        connect=3,  # 连接重试次数
        read=3,  # 读取重试次数
        backoff_factor=0.5,  # 退避因子：0.5秒 * (2 ** (重试次数 - 1))
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
        allowed_methods={"GET", "POST", "PUT", "DELETE"},  # 允许重试的HTTP方法
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    yield session

    # 清理：关闭会话
    session.close()


@pytest.fixture
def driver():
    """
    WebDriver fixture，提供Chrome浏览器实例

    配置：
    - 窗口大小：1920x1080
    - 无头模式：根据HEADLESS环境变量决定
    - 禁用自动化检测：移除"Chrome正在受到自动化测试软件的控制"提示
    - 禁用密码管理器、通知、翻译等干扰功能
    - 优化性能：禁用GPU、扩展、优化提示等

    环境变量：
    - HEADLESS: 是否使用无头模式（默认true）
    - CHROME_DRIVER_PATH: ChromeDriver路径（默认使用Selenium Manager）

    Yields:
        WebDriver: Chrome浏览器驱动实例，已打开BASE_UI_URL

    清理：
        测试结束后自动关闭浏览器

    跳过：
        如果ChromeDriver不可用，跳过测试
    """
    options = Options()

    # 实验性选项：禁用各种干扰功能
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,  # 禁用凭据服务
        "profile.password_manager_enabled": False,  # 禁用密码管理器
        "profile.default_content_setting_values.notifications": 2,  # 禁用通知
        "profile.default_content_setting_values.popups": 2,  # 禁用弹窗
        "translate.enabled": False,  # 禁用翻译
        "safebrowsing.enabled": True,  # 启用安全浏览
    })

    # 排除自动化标志
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    # 根据环境变量决定是否使用无头模式
    if HEADLESS:
        options.add_argument("--headless=new")  # 使用新版无头模式

    # 浏览器参数
    options.add_argument("--window-size=1920,1080")  # 窗口大小
    options.add_argument("--no-sandbox")  # 禁用沙箱（Docker环境需要）
    options.add_argument("--disable-dev-shm-usage")  # 禁用/dev/shm使用（Docker环境需要）
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--disable-notifications")  # 禁用通知
    options.add_argument("--no-first-run")  # 跳过首次运行体验
    options.add_argument("--no-default-browser-check")  # 跳过默认浏览器检查
    options.add_argument("--disable-extensions")  # 禁用扩展

    # 禁用各种功能以提高性能
    options.add_argument(
        "--disable-features=Translate,PasswordLeakDetection,AutofillServerCommunication,"
        "OptimizationHints,MediaRouter"
    )

    try:
        # 根据环境变量决定使用自定义ChromeDriver还是Selenium Manager
        if CHROME_DRIVER_PATH:
            d = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
        else:
            d = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        # ChromeDriver不可用时跳过测试
        pytest.skip(f"Chrome WebDriver is not available in this environment: {exc.msg}")

    # 打开基础URL
    d.get(BASE_UI_URL)
    yield d

    # 清理：关闭浏览器
    d.quit()


@pytest.fixture
def logged_in_driver(driver):
    """
    已登录的WebDriver fixture

    功能：
    - 使用标准用户（standard_user）自动登录
    - 等待产品页面加载完成

    依赖：
    - driver fixture

    Yields:
        WebDriver: 已登录的浏览器实例，当前在产品页面

    使用场景：
        需要登录后才能测试的功能（如购物车、结算等）
    """
    LoginPage(driver).login("standard_user", "secret_sauce")
    ProductsPage(driver).wait_loaded()
    yield driver


@pytest.fixture
def checkout_driver(logged_in_driver):
    """
    已进入结算页面的WebDriver fixture

    功能：
    - 基于logged_in_driver
    - 自动添加背包到购物车
    - 打开购物车并进入结算页面
    - 等待结算页面加载完成

    依赖：
    - logged_in_driver fixture

    Yields:
        WebDriver: 已登录且在结算页面的浏览器实例

    使用场景：
        测试结算流程（填写收货信息、完成订单等）
    """
    ProductsPage(logged_in_driver).add_backpack_to_cart().open_cart()
    CartPage(logged_in_driver).wait_loaded().checkout()
    CheckoutPage(logged_in_driver).wait_loaded()
    yield logged_in_driver
