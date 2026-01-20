# main.py
"""
Run the LeakBase crawler using the framework.
"""

# --------------------------------------------------
# main.py
# --------------------------------------------------
import asyncio
import pandas as pd

from src.web_crawler.core.base_crawler import BaseCrawler
from src.web_crawler.sites.leakbase_adapter import LeakBaseAdapter
from src.utils.configs import Config


async def main():
    crawler = BaseCrawler(adapter=LeakBaseAdapter(), headless=False)
    results = await crawler.crawl()

    df = pd.DataFrame(results)
    df.to_csv(
        Config.OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print(df.head())
    print(f"[INFO] Saved {len(df)} rows to {Config.OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())