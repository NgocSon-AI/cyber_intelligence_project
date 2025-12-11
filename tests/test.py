from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://leakbase.la/")
time.sleep(10)  # chờ JS challenge

posts = driver.find_elements(By.CSS_SELECTOR, "li._xgtIstatistik-satir")

data = []

for post in posts:
    try:
        # Block chứa tiêu đề + tác giả
        konu = post.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--konu")

        # Author
        author = konu.get_attribute("data-author")

        # Các thẻ <a> trong block (thẻ 1 = google, thẻ 2 = bài viết)
        a_tags = konu.find_elements(By.TAG_NAME, "a")
        title = a_tags[1].text.strip()
        link = a_tags[1].get_attribute("href")

        # Prefix / Type
        try:
            post_type = post.find_element(By.CSS_SELECTOR, ".prefix-arbitors").text.strip()
        except:
            post_type = "unknown"

        # Forum category
        forum = post.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--forum a").text.strip()

        # Stats
        replies = post.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--cevap").text.strip()
        views = post.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--goruntuleme").text.strip()

        # Last author
        last_author = post.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--sonYazan a.username").text.strip()

        # Time
        time_str = post.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--zaman time").get_attribute("datetime")

        # -------------------------
        # LẤY CONTENT BÀI VIẾT
        # -------------------------
        # Mở tab mới
        driver.execute_script("window.open(arguments[0]);", link)
        driver.switch_to.window(driver.window_handles[-1])

        time.sleep(3)  # chờ bài load

        try:
            content = driver.find_element(By.CSS_SELECTOR, ".message-body .bbWrapper").text.strip()
        except:
            content = ""

        # Đóng tab và quay lại trang chính
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Lưu
        data.append({
            "title": title,
            "link": link,
            "author": author,
            "type": post_type,
            "forum": forum,
            "replies": replies,
            "views": views,
            "last_reply_by": last_author,
            "time": time_str,
            "content": content
        })

    except Exception as e:
        print("Error:", e)

driver.quit()

df = pd.DataFrame(data)
df.to_csv("leakbase_posts.csv", index=False, encoding="utf-8")
print(df)
