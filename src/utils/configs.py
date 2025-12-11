import os

class Config:
    SCAN_INTERVAL_HOURS = 3

    URL_LIST = [
        "https://example.com/data-leak",
    ]

    TELEGRAM_SOURCES = [
        "https://t.me/example_group",
    ]

    DB_PATH = "data.db"

    # === Alert via Telegram Bot ===
    TELEGRAM_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TG_CHAT_ID")   # ID bạn muốn nhận thông báo