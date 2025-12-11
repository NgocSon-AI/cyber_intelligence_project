# main.py
"""
Run the LeakBase crawler using the framework.
"""

import pandas as pd
from src.web_crawler.core.base_crawler import BaseCrawler
from src.web_crawler.sites.leakbase_adapter import LeakBaseAdapter


def main():
    crawler = BaseCrawler(adapter=LeakBaseAdapter(), headless=False)
    results = crawler.crawl()

    df = pd.DataFrame(results)
    df.to_csv("leakbase_output.csv", index=False, encoding="utf-8")
    print(df)


if __name__ == "__main__":
    main()
