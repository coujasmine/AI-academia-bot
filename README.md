# AI Academia Bot

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/coujasmine/AI-academia-bot/weekly_fetch.yml?label=Weekly%20Fetch)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/github/license/coujasmine/AI-academia-bot)

自动追踪 FT50 和 UTD24 期刊最新发表的学术论文，生成每周文献摘要报告。专注于管理学与创新创业领域。

Automatically tracks the latest publications from FT50 and UTD24 journals, generating weekly literature summary reports with a focus on management, innovation, and entrepreneurship.

## Features

- **Full FT50 + UTD24 Coverage**: Tracks all 50+ journals across both lists with complete ISSN mappings
- **OpenAlex API Integration**: Primary data source with batch query support (100K requests/day)
- **Crossref API Fallback**: Optional secondary source for additional coverage
- **Innovation Focus Mode**: Filter to only track entrepreneurship & innovation-relevant journals
- **Weekly Markdown Reports**: Organized by research domain with abstracts and metadata
- **AI-Powered Summaries**: Optional LLM integration for trend analysis (supports OpenAI-compatible APIs)
- **Notifications**: Email (SMTP) and Feishu/Lark webhook support
- **GitHub Actions Automation**: Scheduled weekly runs with report archival

## Project Structure

```
AI-academia-bot/
├── config/
│   ├── journals.py        # FT50 & UTD24 journal definitions with ISSNs
│   └── settings.py        # App configuration (env-based)
├── src/
│   ├── fetcher.py         # OpenAlex + Crossref paper fetchers
│   ├── report.py          # Markdown report generator
│   ├── archive.py         # Date-based archiving & README index updater
│   └── notify.py          # Email & Feishu notifications
├── archives/              # Archived reports by date (committed to git)
│   └── 2026-02-03/
│       ├── report.md      # Human-readable report
│       └── data.json      # Machine-readable paper data
├── reports/               # Latest report output (gitignored)
├── samples/               # Sample report for reference
├── .github/workflows/
│   └── weekly_fetch.yml   # GitHub Actions weekly automation
├── main.py                # CLI entry point
├── requirements.txt
├── .env.example           # Environment variable template
└── .gitignore
```

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/coujasmine/AI-academia-bot.git
cd AI-academia-bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings (see Configuration section below)
```

### 3. Run

```bash
# Fetch all FT50 + UTD24 papers from the last 7 days
python main.py

# Only innovation & entrepreneurship journals
python main.py --mode innovation

# Custom time range
python main.py --days 14

# With AI summary and notifications
python main.py --ai-summary --notify

# Also use Crossref for additional coverage
python main.py --crossref

# Archive report to archives/YYYY-MM-DD/ and update README index
python main.py --archive

# Full pipeline: fetch, summarize, archive, and notify
python main.py --ai-summary --archive --notify
```

## Configuration

All configuration is done via environment variables (`.env` file):

| Variable | Required | Description |
|---|---|---|
| `OPENALEX_EMAIL` | Recommended | Your email for OpenAlex polite pool (faster responses) |
| `CROSSREF_EMAIL` | Optional | Your email for Crossref polite pool |
| `LLM_API_KEY` | Optional | API key for AI summaries (OpenAI, DeepSeek, etc.) |
| `LLM_BASE_URL` | Optional | LLM API base URL (default: OpenAI) |
| `LLM_MODEL` | Optional | LLM model name (default: gpt-4o-mini) |
| `SMTP_HOST` | Optional | SMTP server for email notifications |
| `SMTP_PORT` | Optional | SMTP port (default: 587) |
| `SMTP_USER` | Optional | SMTP username |
| `SMTP_PASSWORD` | Optional | SMTP password |
| `NOTIFY_EMAIL_TO` | Optional | Recipient email address(es) |
| `FEISHU_WEBHOOK_URL` | Optional | Feishu/Lark webhook URL |
| `FETCH_DAYS` | Optional | Days to look back (default: 7) |
| `FILTER_MODE` | Optional | "all", "innovation", "ft50", "utd24" |

> **Cost Note on AI Summary:** When using `--ai-summary` with `--mode all`, the bot sends up to 30 paper titles and truncated abstracts to your LLM. With `gpt-4o-mini` this typically costs < $0.01 per run. However, if you switch to larger models (e.g., `gpt-4o`, `claude-3.5-sonnet`), expect higher costs. You can control this by adjusting `LLM_MODEL` or using `--mode innovation` to reduce the number of papers sent to the LLM.

## Sample Report Output

Below is an example of the generated weekly report format (see [`samples/sample_report.md`](samples/sample_report.md) for the full example):

```markdown
# Weekly Academic Paper Summary (2026-02-03)

**Generated:** 2026-02-03 16:00:00
**Total papers:** 42
**FT50 papers:** 42 | **UTD24 papers:** 18 | **High innovation relevance:** 15

---

## Entrepreneurship

### 1. [Digital Platform Ecosystems and New Venture Performance](https://doi.org/10.1111/jbv.xxxxx)

**Authors:** Smith, J., Zhang, L., Kumar, R.
**Journal:** Journal of Business Venturing (JBV) | **Published:** 2026-01-28
`FT50` `Innovation-Core`

> This study examines how digital platform ecosystems shape new venture creation
> and performance outcomes. Drawing on ecosystem theory and ...

**Topics:** Digital Platforms, Entrepreneurship, New Ventures
```

## Journal Coverage

### Innovation & Entrepreneurship Core Journals (FT50)

| Journal | Abbr | Category |
|---|---|---|
| Entrepreneurship Theory and Practice | ETP | Entrepreneurship |
| Journal of Business Venturing | JBV | Entrepreneurship |
| Strategic Entrepreneurship Journal | SEJ | Entrepreneurship |
| Research Policy | RP | Innovation & Technology Policy |

### Management & Strategy (FT50 + UTD24)

| Journal | Abbr | Lists |
|---|---|---|
| Academy of Management Journal | AMJ | FT50 + UTD24 |
| Academy of Management Review | AMR | FT50 + UTD24 |
| Administrative Science Quarterly | ASQ | FT50 + UTD24 |
| Strategic Management Journal | SMJ | FT50 + UTD24 |
| Organization Science | OrgSci | FT50 + UTD24 |
| Management Science | MS | FT50 + UTD24 |
| Journal of Management | JOM | FT50 |
| Journal of Management Studies | JMS | FT50 |

Plus 40+ additional journals across Accounting, Finance, Marketing, IS, Operations, Economics, OB/HR, and Ethics.

## GitHub Actions Automation

The bot runs automatically every Monday at 08:00 UTC (16:00 Beijing time) via GitHub Actions.

### Setup

1. Go to your repository **Settings > Secrets and variables > Actions**
2. Add the following secrets:
   - `OPENALEX_EMAIL` (recommended)
   - `LLM_API_KEY` (optional, for AI summaries)
   - `NOTIFY_EMAIL_TO`, `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD` (optional, for email)
   - `FEISHU_WEBHOOK_URL` (optional, for Feishu)

3. The workflow will:
   - Fetch papers from all FT50/UTD24 journals
   - Generate a Markdown report with AI summary
   - Archive to `archives/YYYY-MM-DD/` with both Markdown and JSON
   - Auto-update the History Reports table in README
   - Commit archives + updated README to git
   - Send notifications via configured channels
   - Upload report as a GitHub Actions artifact (90-day retention)

### Manual trigger

You can also trigger the workflow manually from the Actions tab in GitHub.

## API Sources

| Source | Role | Auth | Rate Limit | Batch Support |
|---|---|---|---|---|
| [OpenAlex](https://openalex.org) | Primary | Email (polite pool) | 100K/day | Yes (50 sources) |
| [Crossref](https://www.crossref.org) | Secondary | Email (polite pool) | Dynamic | No |

---

<!-- ARCHIVE_START -->
<!-- Bot will automatically update the history reports table here -->
<!-- ARCHIVE_END -->

## License

MIT License - see [LICENSE](LICENSE) for details.
