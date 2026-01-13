"""
Configuration file for test environment and test data
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Create directories if they don't exist
SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Application URL
BASE_URL = "https://www.saucedemo.com"

# Test Users (Available on SauceDemo)
USERS = {
    "standard": {
        "username": "standard_user",
        "password": "secret_sauce"
    },
    "locked": {
        "username": "locked_out_user",
        "password": "secret_sauce"
    },
    "problem": {
        "username": "problem_user",
        "password": "secret_sauce"
    },
    "performance": {
        "username": "performance_glitch_user",
        "password": "secret_sauce"
    }
}

# Timeouts (in seconds)
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15
PAGE_LOAD_TIMEOUT = 30

# Checkout Test Data
CHECKOUT_INFO = {
    "first_name": "John",
    "last_name": "Doe",
    "postal_code": "12345"
}

# Invalid Credentials for Negative Testing
INVALID_CREDENTIALS = {
    "invalid_user": {
        "username": "invalid_user",
        "password": "wrong_password"
    },
    "empty": {
        "username": "",
        "password": ""
    }
}

# Expected Error Messages
ERROR_MESSAGES = {
    "invalid_credentials": "Epic sadface: Username and password do not match any user in this service",
    "locked_user": "Epic sadface: Sorry, this user has been locked out.",
    "empty_username": "Epic sadface: Username is required",
    "empty_password": "Epic sadface: Password is required"
}

# Product Sort Options
SORT_OPTIONS = {
    "name_asc": "Name (A to Z)",
    "name_desc": "Name (Z to A)",
    "price_asc": "Price (low to high)",
    "price_desc": "Price (high to low)"
}
