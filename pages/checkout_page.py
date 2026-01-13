"""
Checkout Page Object - Contains elements and methods for checkout pages
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Checkout Page Object Class"""

    # Checkout Information Page Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Checkout Overview Page Locators
    ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")

    # Checkout Complete Page Locators
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def __init__(self, driver):
        """Initialize Checkout Page"""
        super().__init__(driver)
        logger.info("Checkout Page initialized")

    def get_page_title(self):
        """
        Get checkout page title
        
        Returns:
            str: Page title
        """
        title = self.get_text(self.PAGE_TITLE)
        logger.info(f"Checkout page title: {title}")
        return title

    # Checkout Information Methods
    def enter_first_name(self, first_name):
        """
        Enter first name
        
        Args:
            first_name (str): First name
        """
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        logger.info(f"Entered first name: {first_name}")

    def enter_last_name(self, last_name):
        """
        Enter last name
        
        Args:
            last_name (str): Last name
        """
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        logger.info(f"Entered last name: {last_name}")

    def enter_postal_code(self, postal_code):
        """
        Enter postal code
        
        Args:
            postal_code (str): Postal code
        """
        self.send_keys(self.POSTAL_CODE_INPUT, postal_code)
        logger.info(f"Entered postal code: {postal_code}")

    def fill_checkout_information(self, first_name, last_name, postal_code):
        """
        Fill complete checkout information form
        
        Args:
            first_name (str): First name
            last_name (str): Last name
            postal_code (str): Postal code
        """
        logger.info("Filling checkout information")
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)

    def click_continue(self):
        """Click continue button"""
        self.click(self.CONTINUE_BUTTON)
        logger.info("Clicked continue button")

    def click_cancel(self):
        """Click cancel button"""
        self.click(self.CANCEL_BUTTON)
        logger.info("Clicked cancel button")

    def get_error_message(self):
        """
        Get error message text
        
        Returns:
            str: Error message
        """
        error_text = self.get_text(self.ERROR_MESSAGE)
        logger.info(f"Checkout error message: {error_text}")
        return error_text

    def is_error_displayed(self):
        """
        Check if error message is displayed
        
        Returns:
            bool: True if error is displayed
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=2)

    # Checkout Overview Methods
    def get_item_total(self):
        """
        Get item total amount
        
        Returns:
            float: Item total
        """
        total_text = self.get_text(self.ITEM_TOTAL)
        # Extract number from "Item total: $29.99"
        total = float(total_text.split('$')[1])
        logger.info(f"Item total: ${total}")
        return total

    def get_tax(self):
        """
        Get tax amount
        
        Returns:
            float: Tax amount
        """
        tax_text = self.get_text(self.TAX)
        # Extract number from "Tax: $2.40"
        tax = float(tax_text.split('$')[1])
        logger.info(f"Tax: ${tax}")
        return tax

    def get_total(self):
        """
        Get total amount
        
        Returns:
            float: Total amount
        """
        total_text = self.get_text(self.TOTAL)
        # Extract number from "Total: $32.39"
        total = float(total_text.split('$')[1])
        logger.info(f"Total: ${total}")
        return total

    def click_finish(self):
        """Click finish button"""
        self.click(self.FINISH_BUTTON)
        logger.info("Clicked finish button")

    # Checkout Complete Methods
    def get_complete_header(self):
        """
        Get checkout complete header text
        
        Returns:
            str: Complete header text
        """
        header = self.get_text(self.COMPLETE_HEADER)
        logger.info(f"Complete header: {header}")
        return header

    def get_complete_text(self):
        """
        Get checkout complete message
        
        Returns:
            str: Complete message text
        """
        text = self.get_text(self.COMPLETE_TEXT)
        logger.info(f"Complete text: {text}")
        return text

    def is_checkout_complete(self):
        """
        Check if checkout is complete
        
        Returns:
            bool: True if checkout is complete
        """
        is_complete = self.is_element_visible(self.COMPLETE_HEADER)
        logger.info(f"Checkout complete: {is_complete}")
        return is_complete

    def click_back_home(self):
        """Click back home button"""
        self.click(self.BACK_HOME_BUTTON)
        logger.info("Clicked back home button")
