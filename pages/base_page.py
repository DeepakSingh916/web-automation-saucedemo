"""
Base Page - Contains common methods for all page objects
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import EXPLICIT_WAIT
from utils.helpers import take_screenshot
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects"""

    def __init__(self, driver):
        """
        Initialize base page
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def find_element(self, locator):
        """
        Find element with wait
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            WebElement: Found element
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            take_screenshot(self.driver, "element_not_found")
            raise

    def find_elements(self, locator):
        """
        Find multiple elements
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            List[WebElement]: List of found elements
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"Elements found: {len(elements)} for {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            return []

    def click(self, locator):
        """
        Click on element
        
        Args:
            locator: Tuple of (By, value)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked on element: {locator}")

    def send_keys(self, locator, text):
        """
        Send keys to element
        
        Args:
            locator: Tuple of (By, value)
            text: Text to send
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Entered text in element: {locator}")

    def get_text(self, locator):
        """
        Get text from element
        
        Args:
            locator: Tuple of (By, value)
            
        Returns:
            str: Element text
        """
        element = self.find_element(locator)
        text = element.text
        logger.debug(f"Got text from element: {locator} = '{text}'")
        return text

    def is_element_visible(self, locator, timeout=5):
        """
        Check if element is visible
        
        Args:
            locator: Tuple of (By, value)
            timeout: Wait timeout in seconds
            
        Returns:
            bool: True if visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        """
        Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url

    def get_page_title(self):
        """
        Get page title
        
        Returns:
            str: Page title
        """
        return self.driver.title

    def scroll_to_element(self, locator):
        """
        Scroll to element
        
        Args:
            locator: Tuple of (By, value)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug(f"Scrolled to element: {locator}")

    def select_from_dropdown_by_text(self, locator, text):
        """
        Select option from dropdown by visible text
        
        Args:
            locator: Tuple of (By, value)
            text: Option text to select
        """
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        logger.info(f"Selected '{text}' from dropdown: {locator}")

    def get_attribute(self, locator, attribute):
        """
        Get element attribute value
        
        Args:
            locator: Tuple of (By, value)
            attribute: Attribute name
            
        Returns:
            str: Attribute value
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute '{attribute}' = '{value}' from {locator}")
        return value
