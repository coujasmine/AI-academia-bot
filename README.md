<p align="center">
  <h1 align="center">📚 Academia Paper Reading</h1>
  <p align="center">
    <strong>自动追踪 FT50 & UTD24 期刊最新论文，生成每周文献摘要报告</strong><br/>
    <sub>Focused on Management, Innovation & Entrepreneurship</sub>
  </p>
  <p align="center">
    <a href="https://github.com/coujasmine/AI-academia-bot/actions"><img src="https://img.shields.io/github/actions/workflow/status/coujasmine/AI-academia-bot/weekly_fetch.yml?label=Weekly%20Fetch&style=flat-square" alt="CI"></a>
    <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square" alt="Python">
    <a href="LICENSE"><img src="https://img.shields.io/github/license/coujasmine/AI-academia-bot?style=flat-square" alt="License"></a>
  </p>
</p>

---

## ✨ Features

| | Feature | Description |
|---|---|---|
| 🔍 | **Full Journal Coverage** | Tracks 50+ journals across FT50 & UTD24 with complete ISSN mappings |
| 🗂️ | **Weekly Archiving** | Papers saved to `archives/YYYY-MM-DD/` (Markdown + JSON), auto-cleanup after 60 days |
| 🤖 | **AI-Powered Summaries** | Optional LLM integration for trend analysis (OpenAI-compatible APIs) |
| ⚡ | **GitHub Actions** | Fully automated — runs every Monday, commits archives, updates README index |
| 🎯 | **Innovation Focus Mode** | Filter to only entrepreneurship & innovation-relevant journals |

## 🚀 Quick Start

**1 — Clone & Install**

```bash
git clone https://github.com/coujasmine/AI-academia-bot.git
cd AI-academia-bot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**2 — Configure**

```bash
cp .env.example .env
# Edit .env — see Configuration below
```

**3 — Run**

```bash
python main.py --archive                        # Default: last 7 days, all journals
python main.py --mode innovation --archive       # Innovation & entrepreneurship only
python main.py --days 14 --ai-summary --archive  # 14-day range + AI summary
```

## ⚙️ Configuration

All settings via `.env` file:

| Variable | Required | Description |
|---|---|---|
| `OPENALEX_EMAIL` | Recommended | Email for OpenAlex polite pool (faster responses) |
| `CROSSREF_EMAIL` | Optional | Email for Crossref polite pool |
| `LLM_API_KEY` | Optional | API key for AI summaries (OpenAI, DeepSeek, etc.) |
| `LLM_BASE_URL` | Optional | LLM API base URL (default: OpenAI) |
| `LLM_MODEL` | Optional | Model name (default: `gpt-4o-mini`, ~$0.01/run) |
| `FILTER_MODE` | Optional | `all` · `innovation` · `ft50` · `utd24` |

## 🏗️ Project Structure

```
AI-academia-bot/
├── config/
│   ├── journals.py       # FT50 & UTD24 journal definitions with ISSNs
│   └── settings.py       # App configuration (env-based)
├── src/
│   ├── fetcher.py        # OpenAlex + Crossref paper fetchers
│   ├── report.py         # Markdown report generator
│   └── archive.py        # Date-based archiving & README index updater
├── archives/             # Archived reports by date (committed to git)
├── samples/              # Sample report for reference
├── .github/workflows/
│   └── weekly_fetch.yml  # GitHub Actions weekly automation
├── main.py               # CLI entry point
└── requirements.txt
```

## 🤖 GitHub Actions

The bot runs **every Monday at 08:00 UTC** (16:00 Beijing time) automatically.

**Setup:** Go to **Settings → Secrets → Actions** and add `OPENALEX_EMAIL`. That's it.

You can also trigger it manually from the **Actions** tab.

## 📖 Data Sources

Papers are fetched from [**OpenAlex**](https://openalex.org) (primary, 100K req/day) with optional [**Crossref**](https://www.crossref.org) fallback. Journal coverage includes core entrepreneurship journals (ETP, JBV, SEJ, RP) and 40+ management/strategy journals — see [`config/journals.py`](config/journals.py) for the full list.

> 📄 See [`samples/sample_report.md`](samples/sample_report.md) for an example of the generated report format.

---

## 📋 History Reports

<!-- HISTORY_START -->
| Date | Report | Data |
|---|---|---|
| 2026-02-05 | [Report](archives/2026-02-05/report.md) | [JSON](archives/2026-02-05/data.json) |
| 2026-02-04 | [Report](archives/2026-02-04/report.md) | [JSON](archives/2026-02-04/data.json) |
<!-- HISTORY_END -->

## License

[MIT](LICENSE)
