# core/selenium_client.py
"""
Selenium WebDriver wrapper.
Handles initialization, safe navigation, waits, and tab management.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumClient:
    """Selenium Client used as a shared browser instance."""

    def __init__(self, headless: bool = False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

    def open_url(self, url: str, delay: float = 3.0):
        """Navigate to a URL and wait for JS to load."""
        self.driver.get(url)
        time.sleep(delay)

    def open_new_tab(self, url: str, delay: float = 2.0):
        """Open a new browser tab and switch to it."""
        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(delay)

    def close_tab(self):
        """Close the current tab and return to the previous one."""
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])

    def quit(self):
        """Shutdown Selenium browser."""
        self.driver.quit()
