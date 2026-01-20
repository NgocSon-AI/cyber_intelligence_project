# src/core/processor.py
"""
Data processing utilities for the Cyber Intelligence application.

This module provides functionality for processing posts including
leak detection, filtering, and result analysis.
"""

from typing import List, Dict, Any

from src.utils.logger import get_logger
from src.utils.exception import DetectionError, DatabaseError, AlertError
from src.detectors.rules_detector import VietnamRelevanceDetector
from src.storage.db_handler import init_database, save_post
from src.alerts.telegram_bot import TelegramAlert

logger = get_logger(__name__)


class DataProcessor:
    """
    Handles data processing operations for the cyber intelligence application.

    This class provides methods for detecting data leaks, filtering results,
    and processing alerts through various channels.
    """

    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the data processor.

        Args:
            bot_token: Telegram bot token for alerts
            chat_id: Telegram chat ID for alerts
        """
        self.logger = logger
        self.detector = VietnamRelevanceDetector()
        self.bot = TelegramAlert(bot_token=bot_token, chat_id=chat_id)

    def detect_data_leaks(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential data leaks in posts using AI detector.

        Args:
            posts: List of post dictionaries to analyze

        Returns:
            List of posts with detection results

        Raises:
            DetectionError: If detection fails
        """
        self.logger.info(f"Analyzing {len(posts)} posts for data leaks...")

        detected_posts = []
        leak_count = 0

        for post in posts:
            try:
                detected_post = self.detector.detect(post)
                detected_posts.append(detected_post)

                if detected_post.get("detect_result", {}).get("label") == "LEAK":
                    leak_count += 1

            except Exception as e:
                error_msg = f"Failed to detect leaks in post"
                self.logger.warning(f"{error_msg}: {e}")
                # Add original post if detection fails
                detected_posts.append(post)

        self.logger.info(
            f"Detection complete: {leak_count} potential leaks found out of {len(posts)} posts"
        )
        return detected_posts

    def filter_leak_posts(self, detected_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter posts that contain potential data leaks.

        Args:
            detected_posts: Posts with detection results

        Returns:
            List of posts classified as containing leaks
        """
        leak_posts = [
            post for post in detected_posts
            if post.get("detect_result", {}).get("label") == "LEAK"
        ]
        self.logger.info(f"Filtered {len(leak_posts)} leak posts for processing")
        return leak_posts

    def initialize_database(self) -> None:
        """
        Initialize the database connection.

        Raises:
            DatabaseError: If database initialization fails
        """
        try:
            init_database()
            self.logger.info("Database initialized successfully")
        except Exception as e:
            error_msg = "Failed to initialize database"
            self.logger.error(f"{error_msg}: {e}")
            raise DatabaseError(error_msg, str(e)) from e

    def process_leak_posts(self, leak_posts: List[Dict[str, Any]]) -> None:
        """
        Process detected leak posts: save to database and send alerts.

        Args:
            leak_posts: Posts containing potential data leaks
        """
        self.logger.info(f"Processing {len(leak_posts)} leak posts...")

        for i, post in enumerate(leak_posts, 1):
            try:
                self.logger.info(f"Processing leak post {i}/{len(leak_posts)}")

                # Save to database
                save_post(post)
                self.logger.debug("Post saved to database")

                # Send Telegram alert
                self.bot.send(post)
                self.logger.debug("Telegram alert sent")

            except Exception as e:
                error_msg = f"Failed to process leak post {i}"
                self.logger.error(f"{error_msg}: {e}")
                # Continue processing other posts even if one fails

        self.logger.info("Leak post processing completed")

    def process_posts(self, posts: List[Dict[str, Any]]) -> None:
        """
        Execute the complete post processing workflow.

        Args:
            posts: Posts to process
        """
        # Step 1: Detect data leaks
        detected_posts = self.detect_data_leaks(posts)

        # Step 2: Filter leak posts
        leak_posts = self.filter_leak_posts(detected_posts)

        # Step 3: Process leak posts if any found
        if leak_posts:
            self.initialize_database()
            self.process_leak_posts(leak_posts)
        else:
            self.logger.info("No data leaks detected")