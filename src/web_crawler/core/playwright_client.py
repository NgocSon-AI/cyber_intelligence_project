# --------------------------------------------------
# core/playwright_client.py
# --------------------------------------------------
# core/playwright_client.py
from playwright.async_api import async_playwright


class PlaywrightClient:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.pw = await async_playwright().start()
        self.browser = await self.pw.chromium.launch(
            headless=self.headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def open(self, url: str):
        await self.page.goto(url)

    async def scroll_until_no_new_posts(
        self,
        selector: str,
        max_round: int = 15,
        delay_ms: int = 1500,
    ):
        last_count = 0

        for _ in range(max_round):
            await self.page.evaluate(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
            await self.page.wait_for_timeout(delay_ms)

            items = await self.page.query_selector_all(selector)
            if len(items) == last_count:
                break
            last_count = len(items)

    async def close(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.pw:
            await self.pw.stop()

