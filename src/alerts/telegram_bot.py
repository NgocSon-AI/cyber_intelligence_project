import requests
from datetime import datetime
from src.utils.logger import get_logger


class TelegramAlert:
    """
    Class gửi cảnh báo về Telegram.

    Args:
        bot_token (str): token bot Telegram
        chat_id (str): chat_id hoặc group_id nhận tin nhắn
    """
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        self.logger = get_logger("TelegramAlert")

    def send(self, post: dict):
        """
        Gửi cảnh báo 1 bài post rủi ro.

        Args:
            post (dict): dict chứa các trường của post, phải có:
                         - source
                         - content
                         - author
                         - detect_result (có label, score, ...)
        """
        detection_date = datetime.now().strftime("%d %b %Y")

        message = (
            "🚨 *DATA LEAK DETECTED*\n\n"
            f"📌 *Source:* {post.get("source", "")}\n"
            f"📌 *Title:* {post.get("title", "")}"
            f"🔗 *Link:* {post.get("link","")}\n"
            f"👤 *Author:* {post.get("author","")}\n"
            f"📅 *Detection Date:* {detection_date}\n"
            f"📂 *Type:* Data leak\n\n"
        )

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(self.api_url, data=payload)
            if response.status_code == 200:
                self.logger.info(f"[TelegramBot] Alert sent successfully for: {post.get('title')}")
            else:
                self.logger.warning(
                    f"[TelegramBot] Failed to send alert for: {post.get('title')}, "
                    f"Status code: {response.status_code}, Response: {response.text}"
                )
        except Exception as e:
            self.logger.error(f"[TelegramBot] Exception when sending alert for: {post.get('title')}, Error: {e}")
