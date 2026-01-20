"""
DarkForums adapter: defines selectors and parsing logic for darkforums.io

This module provides a site-specific adapter for crawling DarkForums forum threads.
The site uses a classic table-based forum structure (MyBB/vBulletin-like).
"""

from typing import List, Dict, Optional
from urllib.parse import urljoin

from src.web_crawler.core.base_adapter import BaseAdapter
from src.utils.configs import Config


class DarkForumsAdapter(BaseAdapter):
    """
    Adapter for crawling and parsing threads from DarkForums.

    This adapter extracts thread links from forum listing tables and parses
    thread detail pages to retrieve title, content, and author.
    """

    BASE_URL: str = Config.DarkForums.BASE_URL

    # ===== Listing selectors =====
    THREAD_TABLE_SELECTOR: str = "table.forum-display__thread-list"
    THREAD_LINK_SELECTOR: str = "a[href^='Thread-']"

    LISTING_LOAD_TIMEOUT: int = Config.DarkForums.LISTING_LOAD_TIMEOUT

    # ===== Detail selectors =====
    TITLE_SELECTOR: str = "span.thread_title, h1"
    CONTENT_SELECTOR: str = "div.post_body, div.post_content"
    AUTHOR_SELECTOR: str = "a.author, span.post_author"

    async def wait_listing_loaded(self, page) -> None:
        """
        Wait until the forum thread table is loaded.
        """
        try:
            await page.wait_for_selector(
                self.THREAD_TABLE_SELECTOR,
                timeout=self.LISTING_LOAD_TIMEOUT
            )
        except Exception as e:
            raise TimeoutError(f"Failed to load DarkForums listing: {e}") from e

    async def get_post_links(self, page) -> List[str]:
        """
        Extract thread URLs from the forum listing table.
        """
        links = set()

        try:
            anchors = await page.query_selector_all(
                f"{self.THREAD_TABLE_SELECTOR} {self.THREAD_LINK_SELECTOR}"
            )

            for a in anchors:
                href = await a.get_attribute("href")
                if not href:
                    continue

                full_url = urljoin(self.BASE_URL, href)
                links.add(full_url)

        except Exception as e:
            print(f"[WARNING] Error extracting DarkForums thread links: {e}")

        return list(links)

    async def parse_detail(self, page) -> Dict[str, Optional[str]]:
        """
        Parse title, content, and author from a thread detail page.
        """
        try:
            title_el = await page.query_selector(self.TITLE_SELECTOR)
            title = (await title_el.text_content()).strip() if title_el else ""

            content_el = await page.query_selector(self.CONTENT_SELECTOR)
            content = (await content_el.text_content()).strip() if content_el else ""

            author_el = await page.query_selector(self.AUTHOR_SELECTOR)
            author = (await author_el.text_content()).strip() if author_el else None

        except Exception as e:
            print(f"[WARNING] Error parsing DarkForums detail: {e}")
            title = ""
            content = ""
            author = None

        return {
            "title": title,
            "content": content,
            "author": author,
        }
