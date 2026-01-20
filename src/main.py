# src/main.py
"""
Main entry point for the Cyber Intelligence Project.

This module provides the application entry point that initializes
and runs the cyber intelligence workflow for detecting data leaks.
"""

import asyncio
from dotenv import load_dotenv

from src.utils.logger import get_logger
from src.utils.exception import MonitoringError
from src.core.workflow import CyberIntelligenceApp

logger = get_logger(__name__)


async def main():
    """
    Main entry point for the cyber intelligence application.

    Supports both CSV processing and live crawling modes.
    Configuration is controlled via environment variables and config files.
    """
    # Load environment variables
    load_dotenv()

    # Configuration: Set to False to enable live crawling
    use_csv_mode = False
    # Configuration: Set to True to save crawled posts to CSV
    save_csv_mode = True

    try:
        app = CyberIntelligenceApp(use_csv=use_csv_mode, save_csv=save_csv_mode)
        await app.run()
    except MonitoringError as e:
        logger.error(f"Application error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
