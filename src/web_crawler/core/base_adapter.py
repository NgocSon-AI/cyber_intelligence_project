# core/base_adapter.py
"""
Base adapter: each site will inherit this class and define selectors.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class BaseAdapter(ABC):
    """Abstract adapter defining what every site must implement."""

    BASE_URL: str = ""

    @abstractmethod
    def get_post_elements(self, driver) -> List:
        """Return list of post elements in the listing page."""
        pass

    @abstractmethod
    def parse_post(self, post_element, driver) -> Dict:
        """Parse a single post block and return structured data."""
        pass
