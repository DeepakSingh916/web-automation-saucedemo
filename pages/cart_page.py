"""
Cart Page Object - Contains elements and methods for cart page
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    """Cart Page Object Class"""

    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")

    def __init__(self, driver):
        """Initialize Cart Page"""
        super().__init__(driver)
        logger.info("Cart Page initialized")

    def get_page_title(self):
        """
        Get cart page title
        
        Returns:
            str: Page title
        """
        title = self.get_text(self.PAGE_TITLE)
        logger.info(f"Cart page title: {title}")
        return title

    def is_page_loaded(self):
        """
        Check if cart page is loaded
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.PAGE_TITLE)

    def get_cart_items_count(self):
        """
        Get number of items in cart
        
        Returns:
            int: Cart items count
        """
        items = self.find_elements(self.CART_ITEMS)
        count = len(items)
        logger.info(f"Cart items count: {count}")
        return count

    def get_cart_item_names(self):
        """
        Get all cart item names
        
        Returns:
            list: List of product names in cart
        """
        elements = self.find_elements(self.CART_ITEM_NAMES)
        names = [element.text for element in elements]
        logger.info(f"Cart item names: {names}")
        return names

    def get_cart_item_prices(self):
        """
        Get all cart item prices
        
        Returns:
            list: List of prices
        """
        elements = self.find_elements(self.CART_ITEM_PRICES)
        prices = [float(element.text.replace('$', '')) for element in elements]
        logger.info(f"Cart item prices: {prices}")
        return prices

    def remove_item_by_index(self, index):
        """
        Remove item from cart by index
        
        Args:
            index (int): Item index (0-based)
        """
        buttons = self.find_elements(self.REMOVE_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
            logger.info(f"Removed item {index} from cart")
        else:
            logger.error(f"Item index {index} out of range")

    def remove_item_by_name(self, product_name):
        """
        Remove item from cart by product name
        
        Args:
            product_name (str): Product name
        """
        button_id = f"remove-{product_name.lower().replace(' ', '-')}"
        button_locator = (By.ID, button_id)
        self.click(button_locator)
        logger.info(f"Removed '{product_name}' from cart")

    def click_continue_shopping(self):
        """Click continue shopping button"""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
        logger.info("Clicked continue shopping")

    def click_checkout(self):
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
        logger.info("Clicked checkout button")

    def is_cart_empty(self):
        """
        Check if cart is empty
        
        Returns:
            bool: True if cart is empty
        """
        count = self.get_cart_items_count()
        is_empty = count == 0
        logger.info(f"Cart empty: {is_empty}")
        return is_empty
