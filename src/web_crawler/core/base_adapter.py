# core/base_adapter.py
"""
Base adapter for web crawler site implementations.

This module defines the abstract base class that all site-specific adapters
must inherit from. It provides a consistent interface for crawling different
websites using Playwright for browser automation.

Classes:
    BaseAdapter: Abstract base class for site adapters
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseAdapter(ABC):
    """
    Abstract base adapter for website crawling implementations.

    This class defines the interface that all site-specific adapters must
    implement. It provides methods for waiting for page loads, extracting
    post links, and parsing individual post details.

    Attributes:
        BASE_URL (str): The base URL of the website to crawl
    """

    BASE_URL: str = ""

    @abstractmethod
    async def wait_listing_loaded(self, page) -> None:
        """
        Wait for the post listing page to fully load.

        This method should ensure that all dynamic content on the listing
        page has been rendered before attempting to extract information.

        Args:
            page: Playwright page object for the listing page

        Raises:
            TimeoutError: If the page fails to load within expected time
        """
        pass

    @abstractmethod
    async def get_post_links(self, page) -> List[str]:
        """
        Extract all post links from the current listing page.

        This method should find and return all URLs pointing to individual
        posts or threads on the current page.

        Args:
            page: Playwright page object for the listing page

        Returns:
            List of post URLs as strings
        """
        pass

    @abstractmethod
    async def parse_detail(self, page) -> Dict:
        """
        Parse detailed information from a single post page.

        This method should extract all relevant information from an individual
        post page, such as title, content, author, date, etc.

        Args:
            page: Playwright page object for the post detail page

        Returns:
            Dictionary containing parsed post information
        """
        pass

