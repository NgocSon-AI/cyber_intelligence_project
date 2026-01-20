# sites/leakbase_adapter.py
"""
LeakBase adapter: defines selectors and parsing logic for leakbase.la

This module provides a site-specific adapter for crawling LeakBase forum posts.
It implements the BaseAdapter interface to extract post information from the
LeakBase website using Playwright for browser automation.

Classes:
    LeakBaseAdapter: Adapter for parsing LeakBase forum content
"""

from typing import List, Dict, Optional
from urllib.parse import urljoin
from src.web_crawler.core.base_adapter import BaseAdapter
from src.utils.configs import Config


class LeakBaseAdapter(BaseAdapter):
    """
    Adapter for crawling and parsing posts from LeakBase forum.

    This adapter handles the specific HTML structure and selectors used by
    the LeakBase website to extract forum post information including titles,
    authors, content, and metadata.

    Attributes:
        BASE_URL (str): The base URL of the LeakBase forum
        LIST_ITEM_SELECTOR (str): CSS selector for post list items
        TITLE_SELECTOR (str): CSS selector for post titles
        CONTENT_SELECTOR (str): CSS selector for post content
        AUTHOR_SELECTOR (str): CSS selector for post authors
    """

    # Configuration from centralized config
    BASE_URL: str = Config.LeakBase.BASE_URL
    LIST_ITEM_SELECTOR: str = Config.LeakBase.LIST_ITEM_SELECTOR
    TITLE_SELECTOR: str = Config.LeakBase.TITLE_SELECTOR
    CONTENT_SELECTOR: str = Config.LeakBase.CONTENT_SELECTOR
    AUTHOR_SELECTOR: str = Config.LeakBase.AUTHOR_SELECTOR
    THREAD_URL_PATTERN: str = Config.LeakBase.THREAD_URL_PATTERN
    LISTING_LOAD_TIMEOUT: int = Config.LeakBase.LISTING_LOAD_TIMEOUT

    async def wait_listing_loaded(self, page) -> None:
        """
        Wait for the post listing page to fully load.

        This method ensures that the dynamic content on the listing page
        has been rendered before attempting to extract post links.

        Args:
            page: Playwright page object

        Raises:
            TimeoutError: If the listing doesn't load within the timeout period
        """
        try:
            await page.wait_for_selector(self.LIST_ITEM_SELECTOR, timeout=self.LISTING_LOAD_TIMEOUT)
        except Exception as e:
            raise TimeoutError(f"Failed to load post listing: {e}") from e

    # async def get_post_links(self, page) -> List[str]:
    #     """
    #     Extract all post links from the current listing page.

    #     This method finds all anchor tags within post list items that contain
    #     thread links and returns them as a deduplicated list.

    #     Args:
    #         page: Playwright page object

    #     Returns:
    #         List of unique post URLs as strings
    #     """
    #     links = set()

    #     try:
    #         # Find all anchor tags within post list items
    #         items = await page.query_selector_all(f"{self.LIST_ITEM_SELECTOR} a")

    #         for anchor in items:
    #             href = await anchor.get_attribute("href")
    #             if href and self.THREAD_URL_PATTERN in href:
    #                 # Convert relative URLs to absolute URLs
    #                 full_url = urljoin(self.BASE_URL, href)
    #                 links.add(full_url)

    #     except Exception as e:
    #         print(f"[WARNING] Error extracting post links: {e}")

    #     return list(links)

    async def get_post_links(self, page) -> List[str]:
        links = set()
        try:
            items = await page.query_selector_all(f"{self.LIST_ITEM_SELECTOR} a")
            for anchor in items:
                href = await anchor.get_attribute("href")
                if href and self.THREAD_URL_PATTERN in href:
                    full_url = urljoin(self.BASE_URL, href)
                    
                    if full_url.endswith('/latest'):
                        full_url = full_url[:-7]
                        if not full_url.endswith('/'):
                            full_url += '/'
                    links.add(full_url)
        except Exception as e:
            print(f"[WARNING] Error extracting post links: {e}")
        return list(links)



    async def parse_detail(self, page) -> Dict[str, Optional[str]]:
        """
        Parse detailed information from a single post page.

        This method extracts the title, content, and other metadata from
        a specific forum post page.

        Args:
            page: Playwright page object for the post detail page

        Returns:
            Dictionary containing parsed post information:
            - title: Post title
            - content: Post content text
            - author: Post author (if available)
        """
        try:
            # Extract title
            title_element = await page.query_selector(self.TITLE_SELECTOR)
            title = await title_element.text_content() if title_element else ""
            title = title.strip() if title else ""

            # Extract content
            content_element = await page.query_selector(self.CONTENT_SELECTOR)
            content = await content_element.text_content() if content_element else ""
            content = content.strip() if content else ""

            # Extract author (selector may need adjustment based on actual HTML)
            author_element = await page.query_selector(self.AUTHOR_SELECTOR)
            author = (await author_element.get_attribute("data-author")
                     if author_element else None)
            author = author.strip() if author else None

        except Exception as e:
            print(f"[WARNING] Error parsing post detail: {e}")
            title = ""
            content = ""
            author = None

        return {
            "title": title,
            "content": content,
            "author": author,
        }
