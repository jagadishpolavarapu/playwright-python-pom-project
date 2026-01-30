import os
from dataclasses import dataclass
from pathlib import Path

def _parse_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}

def _parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default

def _load_dotenv(dotenv_path: Path) -> None:
    if not dotenv_path.exists():
        return
    try:
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip()
                os.environ.setdefault(k, v)
    except Exception:
        pass

@dataclass
class Settings:
    base_url: str = "https://www.testmu.ai/selenium-playground/"
    headless: bool = True
    slow_mo: int = 0
    timeout_ms: int = 30000

    @classmethod
    def load(cls) -> "Settings":
        _load_dotenv(Path.cwd() / ".env")
        base_url = os.getenv("BASE_URL", cls.base_url)
        headless = _parse_bool(os.getenv("HEADLESS"), cls.headless)
        slow_mo = _parse_int(os.getenv("SLOW_MO"), cls.slow_mo)
        timeout_ms = _parse_int(os.getenv("TIMEOUT"), cls.timeout_ms)
        return cls(base_url=base_url, headless=headless, slow_mo=slow_mo, timeout_ms=timeout_ms)
