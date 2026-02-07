"""
Application settings and configuration.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


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

# ── Fetch Settings ────────────────────────────────────────────────────
# How many days back to look for new papers (default: 7 for weekly)
_fetch_days_raw = os.getenv("FETCH_DAYS", "")
FETCH_DAYS = int(_fetch_days_raw) if _fetch_days_raw.strip() else 7

# How many days of archives to keep (default: 60, ~2 months / ~8 weeks)
_retention_raw = os.getenv("ARCHIVE_RETENTION_DAYS", "")
ARCHIVE_RETENTION_DAYS = int(_retention_raw) if _retention_raw.strip() else 60

# Filter mode: "all" = all FT50+UTD24, "innovation" = only high-relevance
FILTER_MODE = os.getenv("FILTER_MODE", "all")
