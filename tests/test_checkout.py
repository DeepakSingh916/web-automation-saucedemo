"""
Checkout Test Cases
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from config.config import USERS, CHECKOUT_INFO
import logging

logger = logging.getLogger(__name__)


@pytest.mark.checkout
@pytest.mark.regression
class TestCheckout:
    """Checkout Test Class"""

    @pytest.fixture(autouse=True)
    def setup_checkout(self, driver):
        """Setup: Login, add products, navigate to checkout"""
        # Login
        login_page = LoginPage(driver)
        username = USERS["standard"]["username"]
        password = USERS["standard"]["password"]
        login_page.login(username, password)

        # Add products
        products_page = ProductsPage(driver)
        products_page.add_product_to_cart_by_index(0)
        products_page.add_product_to_cart_by_index(1)

        # Go to cart and checkout
        products_page.click_cart_icon()
        cart_page = CartPage(driver)
        cart_page.click_checkout()

        yield

    def test_checkout_information_page(self, driver):
        """
        Test Case: Verify checkout information page loads
        Steps:
            1. Navigate to checkout
            2. Verify checkout information page is displayed
        """
        logger.info("Starting test: Checkout Information Page")

        checkout_page = CheckoutPage(driver)

        # Verify page title
        page_title = checkout_page.get_page_title()
        assert "Checkout: Your Information" in page_title, f"Unexpected page title: {page_title}"

        logger.info("Test passed: Checkout Information Page")

    def test_complete_checkout_flow(self, driver):
        """
        Test Case: Verify complete checkout flow
        Steps:
            1. Fill checkout information
            2. Continue to overview
            3. Verify order details
            4. Complete order
            5. Verify order completion
        """
        logger.info("Starting test: Complete Checkout Flow")

        checkout_page = CheckoutPage(driver)

        # Fill checkout information
        checkout_page.fill_checkout_information(
            CHECKOUT_INFO["first_name"],
            CHECKOUT_INFO["last_name"],
            CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()

        # Verify checkout overview page
        assert "Checkout: Overview" in checkout_page.get_page_title(), "Not on overview page"

        # Verify totals exist
        item_total = checkout_page.get_item_total()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()

        assert item_total > 0, "Item total should be greater than 0"
        assert tax > 0, "Tax should be greater than 0"
        assert total > item_total, "Total should include tax"

        # Complete order
        checkout_page.click_finish()

        # Verify order completion
        assert checkout_page.is_checkout_complete(), "Checkout not completed"
        assert "Thank you for your order!" in checkout_page.get_complete_header(), "Completion message not found"

        logger.info("Test passed: Complete Checkout Flow")

    def test_checkout_with_empty_first_name(self, driver):
        """
        Test Case: Verify validation for empty first name
        Steps:
            1. Leave first name empty
            2. Fill other fields
            3. Click continue
            4. Verify error message
        """
        logger.info("Starting test: Empty First Name Validation")

        checkout_page = CheckoutPage(driver)

        # Fill only last name and postal code
        checkout_page.enter_last_name(CHECKOUT_INFO["last_name"])
        checkout_page.enter_postal_code(CHECKOUT_INFO["postal_code"])
        checkout_page.click_continue()

        # Verify error
        assert checkout_page.is_error_displayed(), "Error message not displayed"
        error_message = checkout_page.get_error_message()
        assert "First Name is required" in error_message, f"Unexpected error: {error_message}"

        logger.info("Test passed: Empty First Name Validation")

    def test_checkout_with_empty_last_name(self, driver):
        """
        Test Case: Verify validation for empty last name
        Steps:
            1. Fill first name and postal code
            2. Leave last name empty
            3. Click continue
            4. Verify error message
        """
        logger.info("Starting test: Empty Last Name Validation")

        checkout_page = CheckoutPage(driver)

        # Fill only first name and postal code
        checkout_page.enter_first_name(CHECKOUT_INFO["first_name"])
        checkout_page.enter_postal_code(CHECKOUT_INFO["postal_code"])
        checkout_page.click_continue()

        # Verify error
        assert checkout_page.is_error_displayed(), "Error message not displayed"
        error_message = checkout_page.get_error_message()
        assert "Last Name is required" in error_message, f"Unexpected error: {error_message}"

        logger.info("Test passed: Empty Last Name Validation")

    def test_checkout_with_empty_postal_code(self, driver):
        """
        Test Case: Verify validation for empty postal code
        Steps:
            1. Fill first name and last name
            2. Leave postal code empty
            3. Click continue
            4. Verify error message
        """
        logger.info("Starting test: Empty Postal Code Validation")

        checkout_page = CheckoutPage(driver)

        # Fill only first name and last name
        checkout_page.enter_first_name(CHECKOUT_INFO["first_name"])
        checkout_page.enter_last_name(CHECKOUT_INFO["last_name"])
        checkout_page.click_continue()

        # Verify error
        assert checkout_page.is_error_displayed(), "Error message not displayed"
        error_message = checkout_page.get_error_message()
        assert "Postal Code is required" in error_message, f"Unexpected error: {error_message}"

        logger.info("Test passed: Empty Postal Code Validation")

    def test_cancel_checkout(self, driver):
        """
        Test Case: Verify cancel button on checkout page
        Steps:
            1. Navigate to checkout
            2. Click cancel button
            3. Verify redirected to cart page
        """
        logger.info("Starting test: Cancel Checkout")

        checkout_page = CheckoutPage(driver)
        cart_page = CartPage(driver)

        # Click cancel
        checkout_page.click_cancel()

        # Verify back on cart page
        assert cart_page.is_page_loaded(), "Should be redirected to cart page"

        logger.info("Test passed: Cancel Checkout")

    def test_back_to_home_after_completion(self, driver):
        """
        Test Case: Verify back to home button after order completion
        Steps:
            1. Complete full checkout
            2. Click back to home
            3. Verify on products page
        """
        logger.info("Starting test: Back to Home After Completion")

        checkout_page = CheckoutPage(driver)
        products_page = ProductsPage(driver)

        # Complete checkout
        checkout_page.fill_checkout_information(
            CHECKOUT_INFO["first_name"],
            CHECKOUT_INFO["last_name"],
            CHECKOUT_INFO["postal_code"]
        )
        checkout_page.click_continue()
        checkout_page.click_finish()

        # Click back home
        checkout_page.click_back_home()

        # Verify on products page
        assert products_page.is_page_loaded(), "Should be redirected to products page"

        logger.info("Test passed: Back to Home After Completion")
