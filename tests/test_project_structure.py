def test_page_object_classes_are_available():
    from pages.base_page import BasePage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage
    from pages.login_page import LoginPage
    from pages.products_page import ProductsPage

    assert BasePage.__name__ == "BasePage"
    assert LoginPage.__name__ == "LoginPage"
    assert ProductsPage.__name__ == "ProductsPage"
    assert CartPage.__name__ == "CartPage"
    assert CheckoutPage.__name__ == "CheckoutPage"


def test_cart_navigation_page_objects_wait_for_stable_state():
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage
    from pages.products_page import ProductsPage

    class Link:
        def get_attribute(self, name):
            return "https://www.saucedemo.com/cart.html" if name == "href" else None

    calls = []
    products_page = ProductsPage.__new__(ProductsPage)
    products_page.click = lambda locator: calls.append(("click", locator)) or products_page
    products_page.find = lambda locator: calls.append(("find", locator)) or Link()
    products_page.wait_until_url_contains = lambda value: calls.append(("url", value)) or products_page
    products_page.driver = type("Driver", (), {"get": lambda _, url: calls.append(("get", url))})()

    products_page.add_backpack_to_cart().open_cart()

    assert ("find", ProductsPage.CART_BADGE) in calls
    assert ("get", "https://www.saucedemo.com/cart.html") in calls
    assert ("url", "cart") in calls

    calls = []
    cart_page = CartPage.__new__(CartPage)
    cart_page.click = lambda locator: calls.append(("click", locator)) or cart_page
    cart_page.js_click = lambda locator: calls.append(("js_click", locator)) or cart_page
    cart_page.find = lambda locator: calls.append(("find", locator)) or object()
    cart_page.wait_until_url_contains = lambda value: calls.append(("url", value)) or cart_page

    cart_page.wait_loaded().checkout()

    assert ("find", CartPage.CART_LIST) in calls
    assert ("find", CartPage.CHECKOUT_BUTTON) in calls
    assert ("js_click", CartPage.CHECKOUT_BUTTON) in calls
    assert ("url", "checkout-step-one") in calls

    calls = []
    checkout_page = CheckoutPage.__new__(CheckoutPage)
    checkout_page.find = lambda locator: calls.append(("find", locator)) or object()
    checkout_page.wait_until_url_contains = lambda value: calls.append(("url", value)) or checkout_page

    checkout_page.wait_loaded()

    assert ("url", "checkout-step-one") in calls
