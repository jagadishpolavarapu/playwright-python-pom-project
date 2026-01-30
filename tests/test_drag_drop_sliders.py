from src.pages.selenium_playground_home import SeleniumPlaygroundHome
from src.pages.drag_drop_sliders_page import DragDropSlidersPage

def test_drag_drop_slider_default_15_to_95(page, settings):
    # Open base
    home = SeleniumPlaygroundHome(page, base_url=settings.base_url, default_timeout_ms=settings.timeout_ms).open()
    # 1) Click Drag & Drop Sliders
    page.get_by_role("link", name="Drag & Drop Sliders").click()
    # 2) Set 'Default value 15' slider to 95 and assert
    sliders = DragDropSlidersPage(page, base_url=settings.base_url, default_timeout_ms=settings.timeout_ms)
    sliders.set_default_value_15_slider_to(95).assert_default_value_15_is(95)
