"""
Product Test Cases
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config.config import USERS, SORT_OPTIONS
import logging

logger = logging.getLogger(__name__)


@pytest.mark.products
@pytest.mark.regression
class TestProducts:
    """Product Test Class"""

    @pytest.fixture(autouse=True)
    def login(self, driver):
        """Auto-login before each test"""
        login_page = LoginPage(driver)
        username = USERS["standard"]["username"]
        password = USERS["standard"]["password"]
        login_page.login(username, password)
        yield

    def test_products_display(self, driver):
        """
        Test Case: Verify products are displayed after login
        Steps:
            1. Login with valid credentials
            2. Verify products page is loaded
            3. Verify products are displayed
        """
        logger.info("Starting test: Products Display")

        products_page = ProductsPage(driver)

        # Verify products page
        assert products_page.is_page_loaded(), "Products page not loaded"
        assert products_page.get_page_title() == "Products", "Page title mismatch"

        # Verify products count
        product_count = products_page.get_product_count()
        assert product_count == 6, f"Expected 6 products, found {product_count}"

        logger.info("Test passed: Products Display")

    def test_sort_by_name_asc(self, driver):
        """
        Test Case: Verify sorting products by name (A to Z)
        Steps:
            1. Login and navigate to products page
            2. Sort products by Name (A to Z)
            3. Verify products are sorted correctly
        """
        logger.info("Starting test: Sort by Name A-Z")

        products_page = ProductsPage(driver)

        # Sort products
        products_page.sort_products(SORT_OPTIONS["name_asc"])

        # Get product names
        product_names = products_page.get_all_product_names()

        # Verify sorting
        sorted_names = sorted(product_names)
        assert product_names == sorted_names, f"Products not sorted correctly: {product_names}"

        logger.info("Test passed: Sort by Name A-Z")

    def test_sort_by_name_desc(self, driver):
        """
        Test Case: Verify sorting products by name (Z to A)
        Steps:
            1. Login and navigate to products page
            2. Sort products by Name (Z to A)
            3. Verify products are sorted correctly
        """
        logger.info("Starting test: Sort by Name Z-A")

        products_page = ProductsPage(driver)

        # Sort products
        products_page.sort_products(SORT_OPTIONS["name_desc"])

        # Get product names
        product_names = products_page.get_all_product_names()

        # Verify sorting (reverse alphabetical)
        sorted_names = sorted(product_names, reverse=True)
        assert product_names == sorted_names, f"Products not sorted correctly: {product_names}"

        logger.info("Test passed: Sort by Name Z-A")

    def test_sort_by_price_low_to_high(self, driver):
        """
        Test Case: Verify sorting products by price (low to high)
        Steps:
            1. Login and navigate to products page
            2. Sort products by Price (low to high)
            3. Verify products are sorted correctly
        """
        logger.info("Starting test: Sort by Price Low to High")

        products_page = ProductsPage(driver)

        # Sort products
        products_page.sort_products(SORT_OPTIONS["price_asc"])

        # Get product prices
        product_prices = products_page.get_all_product_prices()

        # Verify sorting
        sorted_prices = sorted(product_prices)
        assert product_prices == sorted_prices, f"Prices not sorted correctly: {product_prices}"

        logger.info("Test passed: Sort by Price Low to High")

    def test_sort_by_price_high_to_low(self, driver):
        """
        Test Case: Verify sorting products by price (high to low)
        Steps:
            1. Login and navigate to products page
            2. Sort products by Price (high to low)
            3. Verify products are sorted correctly
        """
        logger.info("Starting test: Sort by Price High to Low")

        products_page = ProductsPage(driver)

        # Sort products
        products_page.sort_products(SORT_OPTIONS["price_desc"])

        # Get product prices
        product_prices = products_page.get_all_product_prices()

        # Verify sorting (descending)
        sorted_prices = sorted(product_prices, reverse=True)
        assert product_prices == sorted_prices, f"Prices not sorted correctly: {product_prices}"

        logger.info("Test passed: Sort by Price High to Low")

    def test_add_product_to_cart(self, driver):
        """
        Test Case: Verify adding product to cart from products page
        Steps:
            1. Login and navigate to products page
            2. Add first product to cart
            3. Verify cart badge is updated
        """
        logger.info("Starting test: Add Product to Cart")

        products_page = ProductsPage(driver)

        # Initial cart count should be 0
        initial_count = products_page.get_cart_badge_count()
        assert initial_count == 0, "Cart should be empty initially"

        # Add product to cart
        products_page.add_product_to_cart_by_index(0)

        # Verify cart badge updated
        updated_count = products_page.get_cart_badge_count()
        assert updated_count == 1, f"Cart badge should show 1, but shows {updated_count}"

        logger.info("Test passed: Add Product to Cart")

    def test_add_multiple_products_to_cart(self, driver):
        """
        Test Case: Verify adding multiple products to cart
        Steps:
            1. Login and navigate to products page
            2. Add multiple products to cart
            3. Verify cart badge count
        """
        logger.info("Starting test: Add Multiple Products to Cart")

        products_page = ProductsPage(driver)

        # Add 3 products
        products_page.add_product_to_cart_by_index(0)
        products_page.add_product_to_cart_by_index(1)
        products_page.add_product_to_cart_by_index(2)

        # Verify cart badge
        cart_count = products_page.get_cart_badge_count()
        assert cart_count == 3, f"Cart should have 3 items, but has {cart_count}"

        logger.info("Test passed: Add Multiple Products to Cart")
