"""
Login Page Object - Contains elements and methods for login page
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login Page Object Class"""

    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_CLOSE_BUTTON = (By.CSS_SELECTOR, ".error-button")

    def __init__(self, driver):
        """Initialize Login Page"""
        super().__init__(driver)
        logger.info("Login Page initialized")

    def enter_username(self, username):
        """
        Enter username
        
        Args:
            username (str): Username to enter
        """
        self.send_keys(self.USERNAME_INPUT, username)
        logger.info(f"Entered username: {username}")

    def enter_password(self, password):
        """
        Enter password
        
        Args:
            password (str): Password to enter
        """
        self.send_keys(self.PASSWORD_INPUT, password)
        logger.info("Entered password")

    def click_login_button(self):
        """Click login button"""
        self.click(self.LOGIN_BUTTON)
        logger.info("Clicked login button")

    def login(self, username, password):
        """
        Perform login action
        
        Args:
            username (str): Username
            password (str): Password
        """
        logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self):
        """
        Get error message text
        
        Returns:
            str: Error message
        """
        error_text = self.get_text(self.ERROR_MESSAGE)
        logger.info(f"Error message: {error_text}")
        return error_text

    def is_error_displayed(self):
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error is displayed
        """
        return self.is_element_visible(self.ERROR_MESSAGE)

    def close_error_message(self):
        """Close error message"""
        if self.is_error_displayed():
            self.click(self.ERROR_CLOSE_BUTTON)
            logger.info("Closed error message")
