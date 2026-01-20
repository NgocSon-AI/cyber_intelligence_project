# src/core/data_loader.py
"""
Data loading utilities for the Cyber Intelligence application.

This module provides functionality for loading posts from various sources
including CSV files and live web crawling.
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Any

from src.utils.logger import get_logger
from src.utils.exception import MonitoringError
from src.web_crawler.core.base_crawler import BaseCrawler
from src.web_crawler.sites.leakbase_adapter import LeakBaseAdapter
from src.utils.configs import Config

logger = get_logger(__name__)


class DataLoader:
    """
    Handles data loading operations for the cyber intelligence application.

    This class provides methods to load posts from CSV files or perform
    live web crawling to gather data for analysis.
    """

    def __init__(self):
        """Initialize the data loader."""
        self.logger = logger

    def load_posts_from_csv(self, csv_path: str = "") -> List[Dict[str, Any]]:
        """
from src.web_crawler.sites.darkforums_adapter import DarkForumsAdapter
        Load posts from a CSV file.

        Args:
            csv_path: Path to the CSV file containing posts
# Giả sử có rules base check

        Returns:
            List of post dictionaries

        Raises:
            MonitoringError: If CSV loading fails
        """

        try:
            if csv_path is None:
                from src.utils.configs import Config
                csv_path = Config.OUTPUT_PATH
            posts = []
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    post = {
                        "title": row.get("title", "").strip(),
                        "content": row.get("content", "").strip(),
                        "author": (row.get("author", "").strip()
                                 if row.get("author") else None),
                        "link": (row.get("link", "").strip()
                               if row.get("link") else None),
                    }
                    posts.append(post)

            self.logger.info(f"Loaded {len(posts)} posts from CSV file")
            return posts

        except FileNotFoundError as e:
            error_msg = f"CSV file not found: {csv_path}"
            self.logger.error(error_msg)
            raise MonitoringError(error_msg, str(e)) from e
        except csv.Error as e:
            error_msg = f"CSV parsing error in file {csv_path}"
            self.logger.error(error_msg)
            raise MonitoringError(error_msg, str(e)) from e
        except Exception as e:
            error_msg = f"Unexpected error loading CSV file {csv_path}"
            self.logger.error(error_msg)
            raise MonitoringError(error_msg, str(e)) from e

    async def crawl_posts_live(self, mode: str = "darkforums") -> List[Dict[str, Any]]:
        """
        Crawl posts live from configured sources.

        Returns:
            List of crawled post dictionaries

        Raises:
            MonitoringError: If crawling fails
        """
        """
        Crawl posts live from the selected source (LeakBase or DarkForums).
        Args:
            mode: 'leakbase' or 'darkforums'
        Returns:
            List of crawled post dictionaries
        """
        try:
            self.logger.info(f"Starting live post crawling (mode={mode})...")
            if mode == "leakbase":
                from src.web_crawler.sites.leakbase_adapter import LeakBaseAdapter
                adapter = LeakBaseAdapter()
            elif mode == "darkforums":
                from src.web_crawler.sites.darkforums_adapter import DarkForumsAdapter
                adapter = DarkForumsAdapter()
            else:
                raise ValueError(f"Unknown mode: {mode}")
            crawler = BaseCrawler(adapter=adapter, headless=True)
            posts = await crawler.crawl()
            self.logger.info(f"Successfully crawled {len(posts)} posts")
            return posts
        except Exception as e:
            error_msg = "Live crawling failed"
            self.logger.error(f"{error_msg}: {e}")
            raise MonitoringError(error_msg, str(e)) from e

    def save_posts_to_csv(self, posts: List[Dict[str, Any]], csv_path: str = "") -> None:
        """
        Save posts to a CSV file.

        Args:
            posts: List of post dictionaries to save
            csv_path: Path to save the CSV file

        Raises:
            MonitoringError: If CSV saving fails
        """

        try:
            if csv_path is None:
                from src.utils.configs import Config
                csv_path = str(Config.OUTPUT_PATH)
            Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
            with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["title", "content", "author", "link"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write header
                writer.writeheader()

                # Write posts
                for post in posts:
                    writer.writerow({
                        "title": post.get("title", ""),
                        "content": post.get("content", ""),
                        "author": post.get("author", ""),
                        "link": post.get("link", "")
                    })

            self.logger.info(f"Saved {len(posts)} posts to CSV file: {csv_path}")

        except Exception as e:
            error_msg = f"Failed to save posts to CSV file {csv_path}"
            self.logger.error(f"{error_msg}: {e}")
            raise MonitoringError(error_msg, str(e)) from e

    async def load_posts(
        self,
        use_csv: bool = True,
        csv_path: str = "",
        force_update: bool = False,
        mode: str = "darkforums"
    ) -> List[Dict[str, Any]]:
        """
        Load posts using the specified method. If use_csv=True but file không tồn tại hoặc force_update=True, sẽ crawl và lưu lại file CSV.

        Args:
            use_csv: If True, load from CSV; if False, crawl live
            csv_path: Path to CSV file (bắt buộc nếu use_csv=True)
            force_update: Nếu True, luôn crawl mới và overwrite file CSV

        Returns:
            List of post dictionaries
        """
        if use_csv:
            # Nếu không truyền csv_path thì mặc định dùng Config.OUTPUT_PATH
            if not csv_path:
                from src.utils.configs import Config
                csv_path = str(Config.OUTPUT_PATH)
            if force_update or not os.path.exists(csv_path):
                posts = await self.crawl_posts_live(mode=mode)
                self.save_posts_to_csv(posts, csv_path)
                return posts
            else:
                return self.load_posts_from_csv(csv_path)
        else:
            posts = await self.crawl_posts_live(mode=mode)
            if not csv_path:
                from src.utils.configs import Config
                csv_path = str(Config.OUTPUT_PATH)
            self.save_posts_to_csv(posts, csv_path)
            return posts