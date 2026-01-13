"""
Browser configuration and capabilities
"""

# Default browser
DEFAULT_BROWSER = "chrome"

# Browser options
CHROME_OPTIONS = {
    "headless": False,
    "window_size": "maximize",
    "disable_notifications": True,
    "disable_gpu": True,
    "no_sandbox": True,
    "disable_dev_shm_usage": True,
    "arguments": [
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions",
        "--disable-infobars"
    ]
}

FIREFOX_OPTIONS = {
    "headless": False,
    "window_size": "maximize"
}

EDGE_OPTIONS = {
    "headless": False,
    "window_size": "maximize",
    "disable_notifications": True
}

# Supported browsers
SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]
