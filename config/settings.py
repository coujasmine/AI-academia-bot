"""
Application settings and configuration.
"""
import os

def _env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None or str(v).strip() == "":
        return default
    return int(v)

SMTP_PORT = _env_int("SMTP_PORT", 587)

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ── OpenAlex API ───────────────────────────────────────────────────────
# No key required; providing an email gives you access to the "polite pool"
# with faster response times.
OPENALEX_EMAIL = os.getenv("OPENALEX_EMAIL", "")
OPENALEX_BASE_URL = "https://api.openalex.org"

# ── Crossref API (optional secondary source) ──────────────────────────
CROSSREF_EMAIL = os.getenv("CROSSREF_EMAIL", "")
CROSSREF_BASE_URL = "https://api.crossref.org"

# ── LLM for AI-powered summaries (optional) ───────────────────────────
# Supports OpenAI API or any compatible endpoint
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# ── Notification (optional) ───────────────────────────────────────────
# Email
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFY_EMAIL_TO = os.getenv("NOTIFY_EMAIL_TO", "")

# Feishu / Lark webhook (optional)
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")

# ── Fetch Settings ────────────────────────────────────────────────────
# How many days back to look for new papers (default: 7 for weekly)
FETCH_DAYS = int(os.getenv("FETCH_DAYS", "7"))

# Filter mode: "all" = all FT50+UTD24, "innovation" = only high-relevance
FILTER_MODE = os.getenv("FILTER_MODE", "all")
