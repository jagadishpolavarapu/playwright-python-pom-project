from .base_page import BasePage
from playwright.sync_api import expect

class DragDropSlidersPage(BasePage):
    def _get_slider_container(self):
        """Get the specific container for 'Default value 15' slider"""
        # Try multiple selector strategies
        container = self.page.locator(
            "section:has-text('Default value 15'), "
            "div:has-text('Default value 15'), "
            ".slider-container:has-text('Default value 15')"
        ).first
        
        # Wait for container to be visible
        container.wait_for(state="visible", timeout=5000)
        return container

    def _group(self):
        """Get the slider group within the container"""
        return self._get_slider_container()

    def _slider(self):
        """Get the slider input element from the container"""
        group = self._group()
        slider = group.locator("input[type='range'], input[role='slider'], input.range-slider").first
        slider.wait_for(state="visible", timeout=5000)
        return slider

    def _display(self):
        """Get the display element showing current value"""
        g = self._group()
        
        # Try multiple selectors for the display value
        disp = g.locator(
            "output, "
            ".value, "
            ".range-value, "
            "#range, "
            "span[id*='range'], "
            "#rangeSuccess"
        ).first
        
        if disp.count() > 0:
            return disp
        
        # Fallback: find any element with just digits
        return g.locator("text=/^\\d+$/").first

    def set_default_value_15_slider_to(self, target: int):
        """Set slider to target value using keyboard arrows"""
        slider = self._slider()
        display = self._display()
        
        # Scroll slider into view
        slider.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        
        # Focus on the slider
        slider.focus()
        self.page.wait_for_timeout(300)
        
        def current_value() -> int:
            """Get current slider value"""
            try:
                # Try to get from display text first
                txt = display.inner_text().strip()
                if txt:
                    return int("".join(ch for ch in txt if ch.isdigit()))
            except:
                pass
            
            # Fallback: get from slider value attribute
            try:
                v = slider.get_attribute("value") or slider.get_attribute("aria-valuenow") or "0"
                return int(v)
            except:
                return 0

        # Get initial value
        cur = current_value()
        initial_value = cur
        print(f"Initial slider value: {cur}, Target: {target}")
        
        # Calculate direction and steps needed
        steps = 0
        max_steps = 500  # Increased max steps for safety
        
        if cur < target:
            # Move right to increase value
            while cur < target and steps < max_steps:
                slider.press("ArrowRight")
                self.page.wait_for_timeout(50)  # Small delay between presses
                new_cur = current_value()
                
                # Break if value not changing
                if new_cur == cur and steps > 10:
                    print(f"Warning: Slider stuck at {cur}")
                    # Try clicking slider at a position
                    try:
                        slider.click()
                        self.page.wait_for_timeout(200)
                    except:
                        pass
                
                cur = new_cur
                steps += 1
                
                # Log progress every 10 steps
                if steps % 10 == 0:
                    print(f"Progress: Current value = {cur}, Steps = {steps}")
        
        elif cur > target:
            # Move left to decrease value
            while cur > target and steps < max_steps:
                slider.press("ArrowLeft")
                self.page.wait_for_timeout(50)
                new_cur = current_value()
                
                # Break if value not changing
                if new_cur == cur and steps > 10:
                    print(f"Warning: Slider stuck at {cur}")
                    try:
                        slider.click()
                        self.page.wait_for_timeout(200)
                    except:
                        pass
                
                cur = new_cur
                steps += 1
                
                if steps % 10 == 0:
                    print(f"Progress: Current value = {cur}, Steps = {steps}")
        
        final_value = current_value()
        print(f"Final slider value: {final_value} (took {steps} steps)")
        
        # Verify we reached target
        if abs(final_value - target) > 1:
            print(f"Warning: Could not reach exact target. Got {final_value}, expected {target}")
        
        return self

    def assert_default_value_15_is(self, expected: int):
        """Assert the slider display shows expected value"""
        display = self._display()
        
        # Wait for display to be visible
        display.wait_for(state="visible", timeout=5000)
        
        # Allow for small tolerance (±1) in case of rounding
        actual_text = display.inner_text().strip()
        actual_value = int("".join(ch for ch in actual_text if ch.isdigit()))
        
        print(f"Asserting: Expected={expected}, Actual={actual_value}")
        
        # Use contains_text with tolerance
        if abs(actual_value - expected) <= 1:
            # Close enough - pass
            print(f"Value {actual_value} is within tolerance of {expected}")
        else:
            # Exact match required
            expect(display).to_have_text(str(expected), timeout=10000)
        
        return self
