from src.pages.selenium_playground_home import SeleniumPlaygroundHome
from src.pages.simple_form_demo_page import SimpleFormDemoPage

def test_simple_form_demo_steps_2_to_7(page, settings):
    # 1) Open base URL
    home = SeleniumPlaygroundHome(page, base_url=settings.base_url, default_timeout_ms=settings.timeout_ms).open()

    # 2) Click “Simple Form Demo”
    home.open_simple_form_demo()

    # 3) Validate URL contains "simple-form-demo"
    print("After click URL:", page.url)
    simple = SimpleFormDemoPage(page, base_url=settings.base_url, default_timeout_ms=settings.timeout_ms)
    simple.assert_url_contains()

    # 4) Create variable for message
    message = "Welcome to TestMu AI"

    # 5) Enter message in the textbox
    simple.enter_message(message)

    # 6) Click “Get Checked Value” (or fallback)
    simple.click_get_checked_value()

    # 7) Validate message under "Your Message:" section
    simple.assert_message_displayed(message)
