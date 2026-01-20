import os
from pathlib import Path


class Config:
    """
    Configuration class for the cyber intelligence project.

    This class centralizes all configuration constants to avoid hard-coding
    và improve maintainability. All values can be overridden via environment
    variables or configuration files.
    """

    # === DarkForums Site Configuration ===
    class DarkForums:
        """Configuration for DarkForums forum crawling."""
        BASE_URL = os.getenv("DARKFORUMS_BASE_URL", "https://darkforums.io/Forum-Databases")
        LISTING_LOAD_TIMEOUT = int(os.getenv("DARKFORUMS_LISTING_TIMEOUT", 15000))
        THREAD_TABLE_SELECTOR = os.getenv("DARKFORUMS_THREAD_TABLE_SELECTOR", "table.forum-display__thread-list")
        THREAD_LINK_SELECTOR = os.getenv("DARKFORUMS_THREAD_LINK_SELECTOR", "a[href^='Thread-']")
        TITLE_SELECTOR = os.getenv("DARKFORUMS_TITLE_SELECTOR", "span.thread_title, h1")
        CONTENT_SELECTOR = os.getenv("DARKFORUMS_CONTENT_SELECTOR", "div.post_body, div.post_content")
        AUTHOR_SELECTOR = os.getenv("DARKFORUMS_AUTHOR_SELECTOR", "a.author, span.post_author")

    # === General Settings ===
    SCAN_INTERVAL_HOURS = int(os.getenv("SCAN_INTERVAL_HOURS", 3))

    # === Database Settings ===
    DB_PATH = os.getenv("DB_PATH", "data.db")

    # === Web Sources ===
    URL_LIST = [
        os.getenv("EXAMPLE_DATA_LEAK_URL", "https://example.com/data-leak"),
    ]

    # === Telegram Settings ===
    TELEGRAM_SOURCES = [
        os.getenv("TELEGRAM_SOURCE_URL", "https://t.me/example_group"),
    ]

    # === Telegram Bot Alert Settings ===
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # ID bạn muốn nhận thông báo
    BASE_DIR = Path(__file__).resolve().parents[2]
    # === Crawler Settings ===
    # data directory
    DATA_DIR = BASE_DIR / "dataleak"
    DATA_DIR.mkdir(exist_ok=True)

    # file name (từ env)
    OUTPUT_FILE = os.getenv("OUTPUT_FILE", "leakbase_output.csv")

    # full path
    OUTPUT_PATH = DATA_DIR / OUTPUT_FILE

    # === LeakBase Site Configuration ===
    class LeakBase:
        """Configuration for LeakBase forum crawling."""

        BASE_URL = os.getenv("LEAKBASE_BASE_URL", "https://leakbase.la/")

        # Selectors for HTML elements
        LIST_ITEM_SELECTOR = os.getenv("LEAKBASE_LIST_ITEM_SELECTOR", "li._xgtIstatistik-satir")
        TITLE_SELECTOR = os.getenv("LEAKBASE_TITLE_SELECTOR", "h1")
        CONTENT_SELECTOR = os.getenv("LEAKBASE_CONTENT_SELECTOR", ".bbWrapper")
        AUTHOR_SELECTOR = os.getenv("LEAKBASE_AUTHOR_SELECTOR", "[data-author]")

        # Additional selectors (for future use)
        FORUM_SELECTOR = os.getenv("LEAKBASE_FORUM_SELECTOR", "._xgtIstatistik-satir--forum a")
        REPLIES_SELECTOR = os.getenv("LEAKBASE_REPLIES_SELECTOR", "._xgtIstatistik-satir--cevap")
        VIEWS_SELECTOR = os.getenv("LEAKBASE_VIEWS_SELECTOR", "._xgtIstatistik-satir--goruntuleme")
        TIME_SELECTOR = os.getenv("LEAKBASE_TIME_SELECTOR", "._xgtIstatistik-satir--zaman time")
        LAST_AUTHOR_SELECTOR = os.getenv("LEAKBASE_LAST_AUTHOR_SELECTOR", "._xgtIstatistik-satir--sonYazan a.username")

        # Timeouts
        LISTING_LOAD_TIMEOUT = int(os.getenv("LEAKBASE_LISTING_TIMEOUT", 15000))

        # URL patterns
        THREAD_URL_PATTERN = "/threads/"
