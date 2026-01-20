# core/base_crawler.py
"""
Base crawler implementation for orchestrating web scraping operations.

This module provides the main crawler class that coordinates the browser
client and site adapters to extract data from websites. It handles the
overall crawling workflow including page navigation, link extraction,
and data parsing.

Classes:
    BaseCrawler: Main crawler class for web scraping operations
"""

from typing import List, Dict
from src.web_crawler.core.playwright_client import PlaywrightClient
from src.web_crawler.core.base_adapter import BaseAdapter


class BaseCrawler:
    """
    Generic web crawler that orchestrates scraping operations.

    This crawler uses a site-specific adapter to handle the details of
    extracting information from different websites. It manages the browser
    lifecycle and coordinates the crawling process.

    Attributes:
        adapter: Site-specific adapter implementing parsing logic
        client: Browser client for web automation
    """

    def __init__(self, adapter: BaseAdapter, headless: bool = True):
        """
        Initialize the crawler with a site adapter.

        Args:
            adapter: Site-specific adapter for parsing website content
            headless: Whether to run browser in headless mode (default: True)
        """
        self.adapter = adapter
        self.client = PlaywrightClient(headless=headless)

    async def crawl(self) -> List[Dict]:
        """
        Execute the main crawling process.

        This method orchestrates the entire crawling workflow:
        1. Initialize the browser client
        2. Navigate to the listing page
        3. Wait for content to load
        4. Extract post links
        5. Visit each post and parse details
        6. Return collected data

        Returns:
            List of dictionaries containing parsed post information

        Raises:
            Exception: If critical errors occur during crawling
        """
        await self.client.start()
        page = self.client.page

        try:
            # Step 1: Open the main listing page
            await self.client.open(self.adapter.BASE_URL)

            # Step 2: Wait until listing is fully rendered
            await self.adapter.wait_listing_loaded(page)

            # Step 3: Scroll to load all posts (if adapter supports scrolling)
            list_selector = getattr(self.adapter, "LIST_ITEM_SELECTOR", None)
            if list_selector:
                await self.client.scroll_until_no_new_posts(list_selector)

            # Step 4: Extract all post links from the listing
            post_links = await self.adapter.get_post_links(page)
            print(f"[INFO] Found {len(post_links)} posts to crawl")

            results: List[Dict] = []

            # Step 5: Crawl each post detail page
            for idx, link in enumerate(post_links, 1):
                try:
                    print(f"[INFO] Processing post {idx}/{len(post_links)}: {link}")
                    await self.client.open(link)
                    data = await self.adapter.parse_detail(page)
                    data["link"] = link  # Ensure link is included in result
                    results.append(data)
                except Exception as e:
                    print(f"[ERROR] Failed to parse post {link}: {e}")
                    continue

            return results

        finally:
            # Ensure browser is properly closed
            await self.client.close()

