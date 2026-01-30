import re
from playwright.sync_api import Page, expect
from typing import Optional

class BasePage:
    def __init__(self, page: Page, base_url: Optional[str] = None, default_timeout_ms: int = 30000):
        self.page = page
        self.base_url = base_url.rstrip("/") if base_url else None
        self.page.set_default_timeout(default_timeout_ms)

    def goto(self, path: str = "/"):
        if path.startswith("http"):
            url = path
        else:
            if not self.base_url:
                raise ValueError("Base URL is not configured for this page.")
            url = f"{self.base_url}{path}"
        self.page.goto(url)
        return self

    def should_have_url_containing(self, fragment: str):
        pattern = re.compile(rf".*{re.escape(fragment)}.*")
        expect(self.page).to_have_url(pattern)
        return self
