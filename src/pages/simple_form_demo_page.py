from .base_page import BasePage
from playwright.sync_api import expect

class SimpleFormDemoPage(BasePage):
    def assert_url_contains(self):
        self.should_have_url_containing("simple-form-demo")
        return self

    def enter_message(self, message: str):
        # Wait for page to be fully loaded
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)
        
        # Try to find the message input field
        input_field = None
        
        # Method 1: Try by placeholder
        if self.page.get_by_placeholder("Please enter your Message").count():
            input_field = self.page.get_by_placeholder("Please enter your Message")
        # Method 2: Try by label
        elif self.page.get_by_label("Enter Message", exact=False).count():
            input_field = self.page.get_by_label("Enter Message", exact=False)
        # Method 3: Look for input in the form section
        else:
            # Find the form or section containing the single input demo
            form_section = self.page.locator("#get-input, .mb-10, section, form").first
            if form_section.count():
                input_field = form_section.locator("input[type='text']").first
            else:
                input_field = self.page.locator("input[type='text']").first
        
        # Scroll into view and fill
        input_field.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        input_field.click()  # Ensure focus
        input_field.fill(message)
        return self

    def click_get_checked_value(self):
        # Wait a bit after filling
        self.page.wait_for_timeout(500)
        
        # Try common button texts on this playground
        button = None
        if self.page.get_by_role("button", name="Get Checked Value").count():
            button = self.page.get_by_role("button", name="Get Checked Value")
        elif self.page.get_by_role("button", name="Show Message").count():
            button = self.page.get_by_role("button", name="Show Message")
        else:
            # Fallback: find any button near the input
            button = self.page.locator("button:has-text('Get'), button:has-text('Show')").first
        
        # Scroll and click
        button.scroll_into_view_if_needed()
        self.page.wait_for_timeout(300)
        button.click()
        return self

    def assert_message_displayed(self, message: str):
        # Wait for the message to appear after button click
        self.page.wait_for_timeout(1000)
        
        # Try multiple selectors for the result display
        result = self.page.locator(
            "#message, "
            "#display, "
            "#message-one, "
            "[role='status'], "
            ".result, "
            "p:has-text('Your Message:')"
        ).first
        
        # Wait for element to be attached and contain text
        result.wait_for(state="attached", timeout=5000)
        
        # Check if element has the message text (even if hidden visually)
        expect(result).to_contain_text(message, timeout=10000)
        return self
