"""
WebDriver Factory - Manages browser driver creation and configuration
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService, Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager

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
    def _get_chrome_driver(headless: bool = False) -> webdriver.Chrome:
        """
        Initialize Chrome WebDriver with ChromeDriverManager

        Args:
            headless: Whether to run in headless mode

        Returns:
            Chrome WebDriver instance
        """
        options = webdriver.ChromeOptions()

        # Performance options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # ✅ CRITICAL: Use incognito mode - NO saved passwords, NO popups!
        options.add_argument("--incognito")

        # Disable ALL password/credential features
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "autofill.profile_enabled": False
        })

        # Disable automation flags
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)

        # Disable save password prompts
        options.add_argument("--disable-blink-features=AutomationControlled")

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-extensions")

        try:
            # First try local driver
            local_driver_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'drivers',
                'chromedriver.exe'
            )

            if os.path.exists(local_driver_path):
                logger.info(f"Using local ChromeDriver: {local_driver_path}")
                service = Service(local_driver_path)
            else:
                logger.warning(f"Local ChromeDriver not found at {local_driver_path}, using webdriver-manager")

                # Get chromedriver path from manager
                driver_path = ChromeDriverManager().install()

                # Fix: WebDriver Manager may return wrong file
                driver_dir = os.path.dirname(driver_path)
                if not driver_path.endswith('chromedriver.exe'):
                    actual_driver = os.path.join(driver_dir, 'chromedriver.exe')
                    if os.path.exists(actual_driver):
                        driver_path = actual_driver
                        logger.info(f"Fixed driver path to: {driver_path}")

                service = Service(driver_path)

            driver = webdriver.Chrome(service=service, options=options)
            logger.info("Chrome driver initialized successfully")
            return driver

        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise

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
