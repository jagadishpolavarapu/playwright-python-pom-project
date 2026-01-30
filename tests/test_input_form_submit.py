# tests/test_input_form_submit.py
from src.pages.selenium_playground_home import SeleniumPlaygroundHome
from src.pages.input_form_submit_page import InputFormSubmitPage

def test_input_form_submit(page, settings):
    home = SeleniumPlaygroundHome(page, base_url=settings.base_url, default_timeout_ms=settings.timeout_ms).open()
    home.open_input_form_submit()

    form = InputFormSubmitPage(page, base_url=settings.base_url, default_timeout_ms=settings.timeout_ms)
    form.submit_blank_and_assert_error()
    form.fill_form_and_submit(
        name="Madhira Sirisha",
        email="sirisha@example.com",
        password="Secure@1234",
        company="Contoso QA",
        website="https://example.com",
        country_label="United States",
        city="Hyderabad",
        address1="Road No 1",
        address2="Banjara Hills",
        state="Telangana",
        zipcode="500034",
    )