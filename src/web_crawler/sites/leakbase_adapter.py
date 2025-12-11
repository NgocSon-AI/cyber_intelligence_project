# sites/leakbase_adapter.py
"""
LeakBase adapter: defines selectors and parsing logic for leakbase.la
"""

from typing import List, Dict
from selenium.webdriver.common.by import By
from src.web_crawler.core.base_adapter import BaseAdapter


class LeakBaseAdapter(BaseAdapter):
    BASE_URL = "https://leakbase.la/"

    def get_post_elements(self, driver) -> List:
        """Return list of <li> post items on homepage."""
        return driver.find_elements(By.CSS_SELECTOR, "li._xgtIstatistik-satir")

    def parse_post(self, post_element, driver) -> Dict:
        """Parse one post block and return structured info."""
        konu = post_element.find_element(By.CSS_SELECTOR, "._xgtIstatistik-satir--konu")

        # Author
        author = konu.get_attribute("data-author")

        # 2 links inside the block (1 = google link, 2 = real post link)
        a_tags = konu.find_elements(By.TAG_NAME, "a")
        title = a_tags[1].text.strip()
        link = a_tags[1].get_attribute("href")

        # # Type (prefix)
        # try:
        #     post_type = post_element.find_element(
        #         By.CSS_SELECTOR, ".prefix-arbitors"
        #     ).text.strip()
        # except:
        #     post_type = "unknown"

        # # Category
        # forum = post_element.find_element(
        #     By.CSS_SELECTOR, "._xgtIstatistik-satir--forum a"
        # ).text.strip()

        # # Stats
        # replies = post_element.find_element(
        #     By.CSS_SELECTOR, "._xgtIstatistik-satir--cevap"
        # ).text.strip()

        # views = post_element.find_element(
        #     By.CSS_SELECTOR, "._xgtIstatistik-satir--goruntuleme"
        # ).text.strip()

        # Last reply author
        # last_author = post_element.find_element(
        #     By.CSS_SELECTOR, "._xgtIstatistik-satir--sonYazan a.username"
        # ).text.strip()

        time_str = post_element.find_element(
            By.CSS_SELECTOR, "._xgtIstatistik-satir--zaman time"
        ).get_attribute("datetime")

        # -------------------------
        # Load content
        # -------------------------
        driver.execute_script(f"window.open('{link}', '_blank')")
        driver.switch_to.window(driver.window_handles[-1])

        try:
            content = driver.find_element(
                By.CSS_SELECTOR, ".message-body .bbWrapper"
            ).text.strip()
        except:
            content = ""

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        return {
            "title": title,
            "link": link,
            "author": author,
            "time": time_str,
            "content": content,
            "source": "leakbase.la",
        }
