"""
Helper utility functions for tests
"""
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import SCREENSHOTS_DIR, EXPLICIT_WAIT
import logging

logger = logging.getLogger(__name__)


def take_screenshot(driver, test_name):
    """
    Take screenshot and save with timestamp
    
    Args:
        driver: WebDriver instance
        test_name (str): Name of the test
        
    Returns:
        str: Screenshot file path
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)

    try:
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return None


def wait_for_element(driver, locator, timeout=EXPLICIT_WAIT):
    """
    Wait for element to be visible
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
        
    Returns:
        WebElement: Found element
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except Exception as e:
        logger.error(f"Element not found: {locator}, Error: {str(e)}")
        raise


def wait_for_element_clickable(driver, locator, timeout=EXPLICIT_WAIT):
    """
    Wait for element to be clickable
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time in seconds
        
    Returns:
        WebElement: Clickable element
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except Exception as e:
        logger.error(f"Element not clickable: {locator}, Error: {str(e)}")
        raise


def scroll_to_element(driver, element):
    """
    Scroll to element using JavaScript
    
    Args:
        driver: WebDriver instance
        element: WebElement to scroll to
    """
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    logger.debug("Scrolled to element")


def get_element_text(driver, locator, timeout=EXPLICIT_WAIT):
    """
    Get text from element with wait
    
    Args:
        driver: WebDriver instance
        locator: Tuple of (By, value)
        timeout: Maximum wait time
        
    Returns:
        str: Element text
    """
    element = wait_for_element(driver, locator, timeout)
    return element.text
