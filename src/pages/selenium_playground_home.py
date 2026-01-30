# src/pages/selenium_playground_home.py
import re
from playwright.sync_api import expect
from .base_page import BasePage


class SeleniumPlaygroundHome(BasePage):
    """
    Selenium Playground home page.

    Usage:
        home = SeleniumPlaygroundHome(page, base_url="https://www.testmu.ai/selenium-playground").open()
        home.open_simple_form_demo()
        home.open_drag_drop_sliders()
        home.open_input_form_submit()
    """

    # Absolute fallback if base_url is not injected when constructing this page
    ABSOLUTE_HOME = "https://www.testmu.ai/selenium-playground/"
    # Relative path used when base_url is provided
    PATH = "/"

    # ---------------------------
    # Basic navigation helpers
    # ---------------------------
    def open(self):
        """
        Open the Selenium Playground home. Uses base_url if provided; otherwise uses ABSOLUTE_HOME.
        Also asserts we landed on the playground.
        """
        target = self.PATH if self.base_url else self.ABSOLUTE_HOME
        self.goto(target)
        # Accepts both hosts and optional trailing slash
        expect(self.page).to_have_url(re.compile(r".*/selenium-playground/?", re.I))
        return self

    def assert_on_home(self):
        """Assert we are still on/returned to the playground home."""
        expect(self.page).to_have_url(re.compile(r".*/selenium-playground/?", re.I))
        return self

    def _click_nav_and_assert(self, link_name_regex: str, url_regex: str):
        """
        Click a left-nav link by accessible name (regex) and assert URL with regex.
        This tolerates small text/route differences and host switches.
        """
        # Prefer exact role link; use regex name to be robust to spacing/casing
        self.page.get_by_role("link", name=re.compile(link_name_regex, re.I)).click()
        expect(self.page).to_have_url(re.compile(url_regex, re.I))
        return self

    # ---------------------------
    # Scenario-specific entries
    # ---------------------------
    def open_simple_form_demo(self):
        """
        Scenario 1: Open 'Simple Form Demo' and wait for route to contain 'simple-form-demo'.
        """
        return self._click_nav_and_assert(
            r"^\s*Simple\s*Form\s*Demo\s*$",
            r".*simple-form-demo.*",
        )

    def open_drag_drop_sliders(self):
        """
        Scenario 2: Open 'Drag & Drop Sliders' and wait for 'drag-drop-range-sliders-demo' route.
        """
        return self._click_nav_and_assert(
            r"^\s*Drag\s*&\s*Drop\s*Sliders\s*$",
            r".*drag-drop-range-sliders-demo.*",
        )

    def open_input_form_submit(self):
        """
        Scenario 3: Open 'Input Form Submit' and wait for the 'input-form' route.
        (Different variants may use slightly different slugs; we match 'input-form' loosely.)
        """
        return self._click_nav_and_assert(
            r"^\s*Input\s*Form\s*Submit\s*$",
            r".*(input-form).*",
        )