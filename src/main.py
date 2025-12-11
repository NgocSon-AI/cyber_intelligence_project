# from src.detectors.rules_detector import DataLeakDetector

# detector = DataLeakDetector()

# post = """
#     Bán data khách hàng Việt Nam, full info gồm: tên, sđt, email.
#     Có 100k records, giá rẻ, liên hệ Telegram @abcxyz
# """

# result = detector.detect(post)

# print(result)
import os
from src.storage.db_handler import init_database, save_post
from src.web_crawler.core.base_crawler import BaseCrawler
from src.web_crawler.sites.leakbase_adapter import LeakBaseAdapter
from src.detectors.rules_detector import DataLeakDetector
from src.alerts.telegram_bot import TelegramAlert
from dotenv import load_dotenv
from typing import cast
load_dotenv()


TELEGRAM_BOT_TOKEN = cast(str, os.getenv("TELEGRAM_BOT_TOKEN"))
TELEGRAM_CHAT_ID = cast(str, os.getenv("TELEGRAM_CHAT_ID"))

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Vui lòng thiết lập TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID trong .env")

def check_posts_for_leak(posts):
    """
    Chạy DataLeakDetector cho danh sách posts.
    
    Args:
        posts (list[dict]): list các bài post, mỗi post có các trường như title, content, link, author,...
    
    Returns:
        list[dict]: danh sách post đã được gắn kết quả detect_result
    """
    detector = DataLeakDetector()
    checked_posts = []

    for post in posts:
        # Kết hợp title + content để kiểm tra
        text_to_check = f"{post.get('title','')} {post.get('content','')}"
        
        # Chạy detect
        result = detector.detect(text_to_check)
        
        # Gộp post gốc + kết quả detect
        post_with_detect = {**post, "detect_result": result}
        checked_posts.append(post_with_detect)

    return checked_posts

def main():
    crawler = BaseCrawler(adapter=LeakBaseAdapter(), headless=False)
    results = crawler.crawl()
    
    # Chạy check tất cả bài post
    check_results = check_posts_for_leak(results)

    # Lọc ra các post rủi ro (LEAK)
    leak_posts = [post for post in check_results if post["detect_result"]["label"] == "LEAK"]

    # print(f"Tổng bài: {len(check_results)}, Bài rủi ro: {len(leak_posts)}")
    # for post in leak_posts:
    #     print(post["title"], post["detect_result"]["score"])

    init_database()
    for post in leak_posts:
        save_post(post)

    bot = TelegramAlert(bot_token=TELEGRAM_BOT_TOKEN, chat_id=TELEGRAM_CHAT_ID)
    for post in leak_posts:
        bot.send(post)


if __name__ == "__main__":
    main()