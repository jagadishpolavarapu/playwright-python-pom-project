# conftest.py
import os
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from src.utils.config import Settings
from src.utils.logger import get_logger

# -----------------------------------------------------------------------------
# Artifact folders
# -----------------------------------------------------------------------------
_ARTIFACTS = Path("artifacts")
(_ARTIFACTS / "screenshots").mkdir(parents=True, exist_ok=True)
(_ARTIFACTS / "videos").mkdir(parents=True, exist_ok=True)
(_ARTIFACTS / "har").mkdir(parents=True, exist_ok=True)
(_ARTIFACTS / "trace").mkdir(parents=True, exist_ok=True)
(_ARTIFACTS / "console").mkdir(parents=True, exist_ok=True)

logger = get_logger()

# -----------------------------------------------------------------------------
# Settings (loaded once per session)
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def settings() -> Settings:
    s = Settings.load()
    logger.info(
        f"Settings: base_url={s.base_url}, headless={s.headless}, "
        f"slow_mo={s.slow_mo}, timeout_ms={s.timeout_ms}"
    )
    return s

# -----------------------------------------------------------------------------
# Playwright / Browser lifetime
# -----------------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance, settings: Settings):
    # Local, headed/ headless based on Settings
    browser = playwright_instance.chromium.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo
    )
    yield browser
    browser.close()

# -----------------------------------------------------------------------------
# Context per test (video, HAR, tracing)
# -----------------------------------------------------------------------------
@pytest.fixture()
def context(request, browser, settings: Settings):
    test_name = request.node.name.replace("/", "_")

    har_path = (_ARTIFACTS / "har" / f"{test_name}.har").resolve()
    context = browser.new_context(
        record_video_dir=str((_ARTIFACTS / "videos").resolve()),
        record_har_path=str(har_path),
        record_har_omit_content=False,   # keep content for easier debugging
    )
    # Enable tracing (viewable with `playwright show-trace trace.zip`)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    trace_zip = _ARTIFACTS / "trace" / f"{test_name}.zip"
    try:
        context.tracing.stop(path=str(trace_zip))
    except Exception as e:
        logger.error(f"Failed to save trace: {e}")

    context.close()

# -----------------------------------------------------------------------------
# Page per test + console logging
# -----------------------------------------------------------------------------
@pytest.fixture()
def page(request, context, settings: Settings):
    p = context.new_page()
    p.set_default_timeout(settings.timeout_ms)

    test_name = request.node.name.replace("/", "_")
    console_path = (_ARTIFACTS / "console" / f"{test_name}.log")
    console_file = console_path.open("a", encoding="utf-8")

    def _log(msg):
        # NOTE: ConsoleMessage API uses methods .type() and .text()
        try:
            console_file.write(f"{msg.type()}: {msg.text()}\n")
            console_file.flush()
        except Exception:
            # swallow logging errors; do not break the test
            pass

    p.on("console", _log)

    yield p

    try:
        p.close()
    finally:
        console_file.close()

# -----------------------------------------------------------------------------
# On failure: capture screenshot automatically
# -----------------------------------------------------------------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page is not None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            name = item.name.replace("/", "_")
            path = _ARTIFACTS / "screenshots" / f"{name}_{ts}.png"
            try:
                page.screenshot(path=str(path))
                logger.error(f"Saved failure screenshot: {path}")
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")