"""
Pytest configuration and fixtures
"""
import pytest
from utils.driver_factory import DriverFactory
from config.config import BASE_URL
from utils.helpers import take_screenshot
import logging

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    WebDriver fixture - creates and quits driver for each test
    
    Args:
        request: Pytest request object
        
    Yields:
        WebDriver: Browser driver instance
    """
    # Get headless option
    headless = request.config.getoption("--headless")

    # Create driver (Chrome only)
    logger.info(f"Setting up chrome driver (headless: {headless})")
    driver = DriverFactory.get_driver(browser="chrome", headless=headless)

    # Navigate to base URL
    driver.get(BASE_URL)
    logger.info(f"Navigated to: {BASE_URL}")

    # Yield driver to test
    yield driver

    # Teardown
    logger.info("Tearing down driver")
    driver.quit()


@pytest.fixture(scope="function")
def setup_teardown(driver):
    """
    Setup and teardown fixture for tests
    
    Args:
        driver: WebDriver instance
        
    Yields:
        WebDriver: Browser driver instance
    """
    logger.info("Test setup complete")
    yield driver
    logger.info("Test teardown complete")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture screenshot on test failure
    
    Args:
        item: Test item
        call: Test call
    """
    outcome = yield
    report = outcome.get_result()

    # Capture screenshot on failure
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            test_name = item.name
            logger.error(f"Test failed: {test_name}")
            take_screenshot(driver, f"FAILED_{test_name}")


@pytest.fixture(scope="session", autouse=True)
def session_setup():
    """
    Session-level setup - runs once before all tests
    """
    logger.info("=" * 80)
    logger.info("TEST EXECUTION STARTED")
    logger.info("=" * 80)
    yield
    logger.info("=" * 80)
    logger.info("TEST EXECUTION COMPLETED")
    logger.info("=" * 80)
