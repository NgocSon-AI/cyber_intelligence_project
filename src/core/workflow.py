# src/core/workflow.py
"""
Main workflow orchestration for the Cyber Intelligence application.

This module provides the main application class that coordinates
the entire cyber intelligence workflow from data loading to processing.
"""

from typing import List, Dict, Any
from dotenv import load_dotenv
import os

# Load environment variables before importing Config
load_dotenv()

from src.utils.logger import get_logger
from src.utils.exception import ConfigurationError, MonitoringError
from src.utils.configs import Config
from .data_loader import DataLoader
from .processor import DataProcessor

logger = get_logger(__name__)


class CyberIntelligenceApp:
    """
    Main application class for cyber intelligence data leak detection.

    This class encapsulates the entire workflow of crawling, detecting,
    storing, and alerting on potential data leaks.

    Attributes:
        data_loader: Component for loading data from various sources
        processor: Component for processing and analyzing data
        use_csv: Whether to use CSV file instead of live crawling
        save_csv: Whether to save crawled posts to CSV file
    """

    def __init__(self, use_csv: bool = True, save_csv: bool = False, mode: str = "leakbase"):
        """
        Initialize the cyber intelligence application.

        Args:
            use_csv: If True, load posts from CSV file; if False, crawl live
            save_csv: If True, save crawled posts to CSV file (only when use_csv=False)

        Raises:
            ConfigurationError: If required configuration is missing
        """
        self.use_csv = use_csv
        self.save_csv = save_csv
        self.logger = logger
        self.mode = mode

        # Validate configuration
        bot_token = Config.TELEGRAM_BOT_TOKEN
        chat_id = Config.TELEGRAM_CHAT_ID

        if not bot_token or not chat_id:
            raise ConfigurationError(
                "Missing required Telegram configuration. Please set "
                "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables."
            )

        # Initialize components
        self.data_loader = DataLoader()
        self.processor = DataProcessor(bot_token=bot_token, chat_id=chat_id)

        self.logger.info("Cyber Intelligence Application initialized")

    async def run(self) -> None:
        """
        Execute the complete cyber intelligence workflow.

        This method orchestrates the entire process:
        1. Load/crawl posts
        2. Optionally save crawled posts to CSV
        3. Process and analyze posts for data leaks
        4. Store results and send alerts

        Raises:
            MonitoringError: If any step in the workflow fails
        """
        try:
            self.logger.info("Starting Cyber Intelligence workflow")

            # Step 1: Load posts
            posts = await self.data_loader.load_posts(self.use_csv, csv_path=str(Config.OUTPUT_PATH), mode=self.mode)

            if not posts:
                self.logger.warning("No posts to process")
                return

            # Step 2: Save to CSV if requested and crawling was performed
            if self.save_csv and not self.use_csv:
                csv_path = Config.OUTPUT_FILE
                self.data_loader.save_posts_to_csv(posts, csv_path)
                self.logger.info("Posts saved to CSV file")

            # Step 3: Process posts
            self.processor.process_posts(posts)

            self.logger.info("Cyber Intelligence workflow completed successfully")

        except Exception as e:
            error_msg = "Workflow execution failed"
            self.logger.error(f"{error_msg}: {e}")
            raise MonitoringError(error_msg, str(e)) from e