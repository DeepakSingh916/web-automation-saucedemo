"""
Shopping Cart Test Cases
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from config.config import USERS
import logging

logger = logging.getLogger(__name__)


@pytest.mark.cart
@pytest.mark.regression
class TestCart:
    """Shopping Cart Test Class"""

    @pytest.fixture(autouse=True)
    def login_and_add_products(self, driver):
        """Auto-login and add products before each test"""
        # Login
        login_page = LoginPage(driver)
        username = USERS["standard"]["username"]
        password = USERS["standard"]["password"]
        login_page.login(username, password)

        # Add products to cart
        products_page = ProductsPage(driver)
        products_page.add_product_to_cart_by_index(0)
        products_page.add_product_to_cart_by_index(1)

        # Navigate to cart
        products_page.click_cart_icon()
        yield

    def test_cart_page_loaded(self, driver):
        """
        Test Case: Verify cart page loads correctly
        Steps:
            1. Add products to cart
            2. Navigate to cart
            3. Verify cart page is displayed
        """
        logger.info("Starting test: Cart Page Loaded")

        cart_page = CartPage(driver)

        # Verify cart page
        assert cart_page.is_page_loaded(), "Cart page not loaded"
        assert cart_page.get_page_title() == "Your Cart", "Cart page title mismatch"

        logger.info("Test passed: Cart Page Loaded")

    def test_cart_items_display(self, driver):
        """
        Test Case: Verify cart items are displayed
        Steps:
            1. Add products to cart
            2. Navigate to cart
            3. Verify items are displayed in cart
        """
        logger.info("Starting test: Cart Items Display")

        cart_page = CartPage(driver)

        # Verify cart items
        items_count = cart_page.get_cart_items_count()
        assert items_count == 2, f"Expected 2 items in cart, found {items_count}"

        # Verify items have names and prices
        item_names = cart_page.get_cart_item_names()
        assert len(item_names) == 2, "Cart should have 2 item names"

        item_prices = cart_page.get_cart_item_prices()
        assert len(item_prices) == 2, "Cart should have 2 item prices"

        logger.info("Test passed: Cart Items Display")

    def test_remove_item_from_cart(self, driver):
        """
        Test Case: Verify removing item from cart
        Steps:
            1. Add products to cart
            2. Navigate to cart
            3. Remove one item
            4. Verify item is removed
        """
        logger.info("Starting test: Remove Item from Cart")

        cart_page = CartPage(driver)

        # Initial count
        initial_count = cart_page.get_cart_items_count()
        assert initial_count == 2, "Should have 2 items initially"

        # Remove first item
        cart_page.remove_item_by_index(0)

        # Verify count updated
        updated_count = cart_page.get_cart_items_count()
        assert updated_count == 1, f"Should have 1 item after removal, has {updated_count}"

        logger.info("Test passed: Remove Item from Cart")

    def test_remove_all_items(self, driver):
        """
        Test Case: Verify removing all items from cart
        Steps:
            1. Add products to cart
            2. Navigate to cart
            3. Remove all items
            4. Verify cart is empty
        """
        logger.info("Starting test: Remove All Items")

        cart_page = CartPage(driver)

        # Remove all items
        cart_page.remove_item_by_index(0)
        cart_page.remove_item_by_index(0)  # After first removal, second item becomes index 0

        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty"

        logger.info("Test passed: Remove All Items")

    def test_continue_shopping(self, driver):
        """
        Test Case: Verify continue shopping button
        Steps:
            1. Navigate to cart
            2. Click continue shopping
            3. Verify redirected to products page
        """
        logger.info("Starting test: Continue Shopping")

        cart_page = CartPage(driver)
        products_page = ProductsPage(driver)

        # Click continue shopping
        cart_page.click_continue_shopping()

        # Verify back on products page
        assert products_page.is_page_loaded(), "Should be redirected to products page"

        logger.info("Test passed: Continue Shopping")

    def test_proceed_to_checkout(self, driver):
        """
        Test Case: Verify checkout button navigates to checkout page
        Steps:
            1. Add items to cart
            2. Navigate to cart
            3. Click checkout button
            4. Verify checkout page loads
        """
        logger.info("Starting test: Proceed to Checkout")

        from pages.checkout_page import CheckoutPage

        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # Click checkout
        cart_page.click_checkout()

        # Verify checkout page
        assert "Checkout: Your Information" in checkout_page.get_page_title(), "Checkout page not loaded"

        logger.info("Test passed: Proceed to Checkout")
