"""
Login Test Cases
"""
import pytest
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from config.config import USERS, INVALID_CREDENTIALS, ERROR_MESSAGES
import logging

logger = logging.getLogger(__name__)


@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    """Login Test Class"""

    def test_valid_login(self, driver):
        """
        Test Case: Verify login with valid credentials
        Steps:
            1. Enter valid username
            2. Enter valid password
            3. Click login button
            4. Verify products page is displayed
        """
        logger.info("Starting test: Valid Login")

        # Initialize pages
        login_page = LoginPage(driver)
        products_page = ProductsPage(driver)

        # Perform login
        username = USERS["standard"]["username"]
        password = USERS["standard"]["password"]
        login_page.login(username, password)

        # Verify products page is loaded
        assert products_page.is_page_loaded(), "Products page not loaded after login"
        assert "Products" in products_page.get_page_title(), "Products page title mismatch"

        logger.info("Test passed: Valid Login")

    def test_invalid_username(self, driver):
        """
        Test Case: Verify login with invalid username
        Steps:
            1. Enter invalid username
            2. Enter valid password
            3. Click login button
            4. Verify error message is displayed
        """
        logger.info("Starting test: Invalid Username")

        login_page = LoginPage(driver)

        # Attempt login with invalid credentials
        username = INVALID_CREDENTIALS["invalid_user"]["username"]
        password = INVALID_CREDENTIALS["invalid_user"]["password"]
        login_page.login(username, password)

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_text = login_page.get_error_message()
        assert ERROR_MESSAGES["invalid_credentials"] in error_text, f"Unexpected error message: {error_text}"

        logger.info("Test passed: Invalid Username")

    def test_invalid_password(self, driver):
        """
        Test Case: Verify login with invalid password
        Steps:
            1. Enter valid username
            2. Enter invalid password
            3. Click login button
            4. Verify error message is displayed
        """
        logger.info("Starting test: Invalid Password")

        login_page = LoginPage(driver)

        # Attempt login with invalid password
        username = USERS["standard"]["username"]
        password = "wrong_password"
        login_page.login(username, password)

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_text = login_page.get_error_message()
        assert ERROR_MESSAGES["invalid_credentials"] in error_text, f"Unexpected error message: {error_text}"

        logger.info("Test passed: Invalid Password")

    def test_empty_credentials(self, driver):
        """
        Test Case: Verify login with empty credentials
        Steps:
            1. Leave username empty
            2. Leave password empty
            3. Click login button
            4. Verify error message is displayed
        """
        logger.info("Starting test: Empty Credentials")

        login_page = LoginPage(driver)

        # Attempt login with empty credentials
        login_page.click_login_button()

        # Verify error message
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_text = login_page.get_error_message()
        assert ERROR_MESSAGES["empty_username"] in error_text, f"Unexpected error message: {error_text}"

        logger.info("Test passed: Empty Credentials")

    def test_locked_user(self, driver):
        """
        Test Case: Verify login with locked user
        Steps:
            1. Enter locked user credentials
            2. Click login button
            3. Verify locked user error message
        """
        logger.info("Starting test: Locked User")

        login_page = LoginPage(driver)

        # Attempt login with locked user
        username = USERS["locked"]["username"]
        password = USERS["locked"]["password"]
        login_page.login(username, password)

        # Verify locked user error
        assert login_page.is_error_displayed(), "Error message not displayed"
        error_text = login_page.get_error_message()
        assert ERROR_MESSAGES["locked_user"] in error_text, f"Unexpected error message: {error_text}"

        logger.info("Test passed: Locked User")
