"""
WebDriver Factory - Manages browser driver creation and configuration
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from config.browser_config import *
from config.config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT, PROJECT_ROOT
import logging
import os

logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class to create WebDriver instances"""

    @staticmethod
    def get_driver(browser=DEFAULT_BROWSER, headless=False):
        """
        Create and return a WebDriver instance
        
        Args:
            browser (str): Browser name (chrome, firefox, edge)
            headless (bool): Run browser in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = browser.lower()

        if browser not in SUPPORTED_BROWSERS:
            raise ValueError(f"Browser '{browser}' not supported. Choose from {SUPPORTED_BROWSERS}")

        logger.info(f"Initializing {browser} driver (headless: {headless})")

        if browser == "chrome":
            driver = DriverFactory._get_chrome_driver(headless)
        elif browser == "firefox":
            driver = DriverFactory._get_firefox_driver(headless)
        elif browser == "edge":
            driver = DriverFactory._get_edge_driver(headless)

        # Set timeouts
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

        # Maximize window (if not headless)
        if not headless:
            driver.maximize_window()

        logger.info(f"{browser.capitalize()} driver initialized successfully")
        return driver

    @staticmethod
    def _get_chrome_driver(headless):
        """Create Chrome driver"""
        options = webdriver.ChromeOptions()

        # Apply chrome options
        if headless or CHROME_OPTIONS["headless"]:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        if CHROME_OPTIONS["disable_notifications"]:
            options.add_argument("--disable-notifications")

        if CHROME_OPTIONS["disable_gpu"]:
            options.add_argument("--disable-gpu")

        if CHROME_OPTIONS["no_sandbox"]:
            options.add_argument("--no-sandbox")

        if CHROME_OPTIONS["disable_dev_shm_usage"]:
            options.add_argument("--disable-dev-shm-usage")

        # Additional arguments
        for arg in CHROME_OPTIONS["arguments"]:
            options.add_argument(arg)

        # Exclude automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Use local chromedriver from project folder
        chromedriver_path = os.path.join(PROJECT_ROOT, "drivers", "chromedriver.exe")
        
        if os.path.exists(chromedriver_path):
            logger.info(f"Using local ChromeDriver: {chromedriver_path}")
            service = ChromeService(executable_path=chromedriver_path)
        else:
            # Fallback to webdriver-manager if local driver not found
            logger.warning(f"Local ChromeDriver not found at {chromedriver_path}, using webdriver-manager")
            from webdriver_manager.chrome import ChromeDriverManager
            service = ChromeService(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    @staticmethod
    def _get_firefox_driver(headless):
        """Create Firefox driver"""
        options = webdriver.FirefoxOptions()

        if headless or FIREFOX_OPTIONS["headless"]:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        from webdriver_manager.firefox import GeckoDriverManager
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        return driver

    @staticmethod
    def _get_edge_driver(headless):
        """Create Edge driver"""
        options = webdriver.EdgeOptions()

        if headless or EDGE_OPTIONS["headless"]:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")

        if EDGE_OPTIONS["disable_notifications"]:
            options.add_argument("--disable-notifications")

        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

        return driver
