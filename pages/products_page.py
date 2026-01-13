"""
Products Page Object - Contains elements and methods for products page
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    """Products Page Object Class"""

    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    PRODUCT_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    HAMBURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        """Initialize Products Page"""
        super().__init__(driver)
        logger.info("Products Page initialized")

    def get_page_title(self):
        """
        Get products page title
        
        Returns:
            str: Page title
        """
        title = self.get_text(self.PAGE_TITLE)
        logger.info(f"Page title: {title}")
        return title

    def is_page_loaded(self):
        """
        Check if products page is loaded
        
        Returns:
            bool: True if page is loaded
        """
        is_loaded = self.is_element_visible(self.PAGE_TITLE)
        logger.info(f"Products page loaded: {is_loaded}")
        return is_loaded

    def sort_products(self, sort_option):
        """
        Sort products by option
        
        Args:
            sort_option (str): Sort option text
        """
        self.select_from_dropdown_by_text(self.PRODUCT_SORT_DROPDOWN, sort_option)
        logger.info(f"Sorted products by: {sort_option}")

    def get_product_count(self):
        """
        Get total number of products
        
        Returns:
            int: Product count
        """
        products = self.find_elements(self.PRODUCT_ITEMS)
        count = len(products)
        logger.info(f"Total products: {count}")
        return count

    def get_all_product_names(self):
        """
        Get all product names
        
        Returns:
            list: List of product names
        """
        elements = self.find_elements(self.PRODUCT_NAMES)
        names = [element.text for element in elements]
        logger.info(f"Product names: {names}")
        return names

    def get_all_product_prices(self):
        """
        Get all product prices
        
        Returns:
            list: List of prices as floats
        """
        elements = self.find_elements(self.PRODUCT_PRICES)
        # Remove $ sign and convert to float
        prices = [float(element.text.replace('$', '')) for element in elements]
        logger.info(f"Product prices: {prices}")
        return prices

    def add_product_to_cart_by_index(self, index):
        """
        Add product to cart by index
        
        Args:
            index (int): Product index (0-based)
        """
        buttons = self.find_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
            logger.info(f"Added product {index} to cart")
        else:
            logger.error(f"Product index {index} out of range")

    def add_product_to_cart_by_name(self, product_name):
        """
        Add product to cart by name
        
        Args:
            product_name (str): Product name
        """
        # Generate button ID from product name
        button_id = f"add-to-cart-{product_name.lower().replace(' ', '-')}"
        button_locator = (By.ID, button_id)
        self.click(button_locator)
        logger.info(f"Added '{product_name}' to cart")

    def get_cart_badge_count(self):
        """
        Get cart badge count
        
        Returns:
            int: Cart items count
        """
        if self.is_element_visible(self.CART_BADGE, timeout=2):
            count_text = self.get_text(self.CART_BADGE)
            count = int(count_text)
            logger.info(f"Cart badge count: {count}")
            return count
        else:
            logger.info("Cart badge not visible (cart is empty)")
            return 0

    def click_cart_icon(self):
        """Click shopping cart icon"""
        self.click(self.CART_ICON)
        logger.info("Clicked cart icon")

    def logout(self):
        """Perform logout"""
        self.click(self.HAMBURGER_MENU)
        self.click(self.LOGOUT_LINK)
        logger.info("Logged out successfully")
