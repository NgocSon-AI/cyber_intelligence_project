# core/base_crawler.py
"""
The Crawler orchestrates loading pages, using the adapter, 
and returning unified structured results.
"""

from typing import List, Dict
from src.web_crawler.core.selenium_client import SeleniumClient
from src.web_crawler.core.base_adapter import BaseAdapter


class BaseCrawler:
    """Generic crawler that delegates parsing logic to a site adapter."""

    def __init__(self, adapter: BaseAdapter, headless: bool = False):
        self.adapter = adapter
        self.client = SeleniumClient(headless=headless)
        self.results: List[Dict] = []

    def crawl(self) -> List[Dict]:
        """Main crawl entry point."""
        self.client.open_url(self.adapter.BASE_URL, delay=7)

        post_elements = self.adapter.get_post_elements(self.client.driver)

        for post in post_elements:
            try:
                parsed = self.adapter.parse_post(post, self.client.driver)
                self.results.append(parsed)
            except Exception as e:
                print(f"[ERROR] Cannot parse post: {e}")

        self.client.quit()
        return self.results
