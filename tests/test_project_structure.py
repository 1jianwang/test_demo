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
