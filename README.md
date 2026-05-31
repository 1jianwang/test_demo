# 电商平台自动化测试项目

这是一个电商业务场景自动化测试项目，测试目标使用公开练习站点 [SauceDemo](https://www.saucedemo.com/) 和接口练习服务 [JSONPlaceholder](https://jsonplaceholder.typicode.com/)。

项目覆盖登录、商品列表、购物车、下单结算和用户接口 CRUD 场景，使用 Pytest、Selenium WebDriver、Page Object、Allure 报告和 GitHub Actions 搭建自动化测试流程。

## 技术栈

- Python 3.12
- Pytest
- Selenium WebDriver
- Page Object Model
- Requests
- Allure Pytest
- GitHub Actions

## 项目结构

```text
.
├── api_test/                 # 接口自动化测试用例
├── pages/                    # UI 自动化 Page Object 封装
│   ├── base_page.py          # 公共等待、点击、输入、取文本方法
│   ├── login_page.py         # 登录页对象
│   ├── products_page.py      # 商品页对象
│   ├── cart_page.py          # 购物车页对象
│   └── checkout_page.py      # 结算页对象
├── ui_test/                  # UI 自动化测试用例
├── tests/                    # 项目结构约束测试
├── conftest.py               # Pytest fixture、浏览器配置、失败截图
├── pytest.ini                # Pytest 配置
├── requirements.txt          # Python 依赖
└── .github/workflows/test.yml
```

## 环境变量

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| `BASE_UI_URL` | `https://www.saucedemo.com` | UI 测试目标地址 |
| `BASE_API_URL` | `https://jsonplaceholder.typicode.com` | API 测试目标地址 |
| `HEADLESS` | `true` | 是否使用无头浏览器 |
| `CHROME_DRIVER_PATH` | 空 | 可选，手动指定 ChromeDriver 路径 |

## 本地运行

```bash
pip install -r requirements.txt
pytest api_test -v
pytest ui_test -v
```

生成 Allure 结果：

```bash
pytest --alluredir=allure-results
```

如果本地已安装 Allure 命令行，可以查看报告：

```bash
allure serve allure-results
```

## 覆盖场景

- 登录：正常登录、错误用户名、错误密码、空值、超长输入、特殊字符、封禁账号。
- 商品：商品信息展示、名称排序、价格排序、商品详情、加入购物车、移除商品。
- 下单：购物车进入结算、必填项校验、正常提交订单、取消下单。
- 接口：查询用户、查询不存在用户、新增用户、修改用户、删除用户。

## 工程亮点

- 使用 Page Object Model 分离页面操作和测试断言，提升用例可维护性。
- `conftest.py` 统一管理浏览器、接口 Session、登录态和结算前置流程。
- 用例通过 Allure 的 feature、story、severity、title 描述测试意图。
- 失败时自动截图并写入 Allure 附件，便于定位 UI 问题。
- GitHub Actions 将 API 测试和 UI 测试拆分为两个 job，并在失败时保留 Allure 结果。
