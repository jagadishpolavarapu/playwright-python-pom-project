# Playwright + Python (Pytest) — POM (Simple Form Demo: Steps 2–7)

This project opens TestMu AI's Selenium Playground and completes Steps 2–7 of the **Simple Form Demo** scenario.

## Quick Start
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install

# Run headed to watch the browser
set HEADLESS=false & set SLOW_MO=400 & pytest -v -k test_simple_form_demo
```

## Artifacts
- Videos            → `artifacts/videos/`
- Playwright traces → `artifacts/trace/<test>.zip` (open with `python -m playwright show-trace artifacts/trace/<test>.zip`)
- Network HAR       → `artifacts/har/<test>.har`
- Console logs      → `artifacts/console/<test>.log`
- Screenshots (fail)→ `artifacts/screenshots/`

## Config
Default `BASE_URL`: `https://www.testmu.ai/selenium-playground/`
You can override via `.env`.

## Tests
- `tests/test_simple_form_demo.py` implements Steps 2–7.


---

## Scenario commands
Run headed to watch the flows:
```bash
# Scenario 1 (Simple Form Demo)
HEADLESS=false SLOW_MO=400 pytest -v -k test_simple_form_demo

# Scenario 2 (Drag & Drop Sliders)
HEADLESS=false SLOW_MO=300 pytest -v -k test_drag_drop_sliders

# Scenario 3 (Input Form Submit)
HEADLESS=false SLOW_MO=300 pytest -v -k test_input_form_submit
```
