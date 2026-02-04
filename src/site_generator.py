"""
Static site generator for GitHub Pages.

Reads archived paper data (archives/*/data.json) and generates a set of
static HTML pages under docs/ that can be served by GitHub Pages.

Pages generated:
  - docs/index.html        Main page with week list and aggregate stats
  - docs/week/YYYY-MM-DD.html   Detail page for each weekly archive
"""

import json
import logging
import re
from html import escape
from pathlib import Path

from config.settings import BASE_DIR

logger = logging.getLogger(__name__)

ARCHIVES_DIR = BASE_DIR / "archives"
DOCS_DIR = BASE_DIR / "docs"
WEEK_DIR = DOCS_DIR / "week"

CATEGORY_ORDER = [
    "Entrepreneurship",
    "Innovation & Technology Policy",
    "Management",
    "Strategy",
    "Organization",
    "Management Science",
    "International Business",
    "Practitioner",
    "Marketing",
    "Information Systems",
    "Operations Management",
    "Operations Research",
    "OB & HR",
    "Accounting",
    "Finance",
    "Economics",
    "Ethics",
]


def generate_site():
    """Generate the full static site from archived data."""
    WEEK_DIR.mkdir(parents=True, exist_ok=True)

    weeks = _load_all_weeks()
    if not weeks:
        logger.warning("No archive data found, skipping site generation")
        return

    _generate_index(weeks)
    for date_str, papers in weeks.items():
        _generate_week_page(date_str, papers)

    logger.info("Site generated: %d week pages in docs/", len(weeks))


def _load_all_weeks() -> dict[str, list[dict]]:
    """Load all weekly archives, sorted newest first."""
    weeks = {}
    if not ARCHIVES_DIR.exists():
        return weeks

    for d in sorted(ARCHIVES_DIR.iterdir(), reverse=True):
        if not d.is_dir() or not re.match(r"\d{4}-\d{2}-\d{2}", d.name):
            continue
        json_path = d / "data.json"
        if json_path.exists():
            try:
                papers = json.loads(json_path.read_text(encoding="utf-8"))
                weeks[d.name] = papers
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Failed to load %s: %s", json_path, e)
    return weeks


def _generate_index(weeks: dict[str, list[dict]]):
    """Generate the main index page with week list."""
    total_papers = sum(len(p) for p in weeks.values())
    total_weeks = len(weeks)

    week_rows = []
    for date_str, papers in weeks.items():
        ft50 = sum(1 for p in papers if p.get("in_ft50"))
        utd24 = sum(1 for p in papers if p.get("in_utd24"))
        high = sum(1 for p in papers if p.get("innovation_relevance") == "high")
        week_rows.append(f"""
      <li class="week-item">
        <div>
          <a href="week/{date_str}.html">{date_str}</a>
        </div>
        <div class="week-meta">
          {len(papers)} papers &middot; FT50: {ft50} &middot; UTD24: {utd24} &middot; Innovation: {high}
        </div>
      </li>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Academia Bot - Weekly Paper Archive</title>
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <header>
    <h1>AI Academia Bot</h1>
    <p>FT50 &amp; UTD24 Weekly Paper Archive &middot; Management, Innovation &amp; Entrepreneurship</p>
    <div class="stats">
      <div class="stat">
        <div class="stat-value">{total_weeks}</div>
        <div class="stat-label">Weeks Archived</div>
      </div>
      <div class="stat">
        <div class="stat-value">{total_papers}</div>
        <div class="stat-label">Total Papers</div>
      </div>
    </div>
  </header>

  <div class="container">
    <h2>Weekly Archives</h2>
    <ul class="week-list">
      {"".join(week_rows)}
    </ul>
  </div>

  <footer>
    Powered by <a href="https://openalex.org">OpenAlex</a> &middot;
    <a href="https://github.com/coujasmine/AI-academia-bot">GitHub</a>
  </footer>
</body>
</html>"""

    (DOCS_DIR / "index.html").write_text(html, encoding="utf-8")
    logger.info("Generated index.html (%d weeks)", total_weeks)


def _generate_week_page(date_str: str, papers: list[dict]):
    """Generate the detail page for a single week."""
    grouped = _group_papers(papers)

    ft50_count = sum(1 for p in papers if p.get("in_ft50"))
    utd24_count = sum(1 for p in papers if p.get("in_utd24"))
    high_count = sum(1 for p in papers if p.get("innovation_relevance") == "high")

    sections = []
    for cat, cat_papers in grouped.items():
        cards = []
        for p in cat_papers:
            cards.append(_render_paper_card(p))
        sections.append(f"""
    <div class="category-section" data-category="{escape(cat)}">
      <h2>{escape(cat)} ({len(cat_papers)})</h2>
      {"".join(cards)}
    </div>""")

    # Build filter buttons from categories present
    filter_btns = ['<button class="filter-btn active" data-filter="all">All</button>']
    for cat in grouped:
        filter_btns.append(
            f'<button class="filter-btn" data-filter="{escape(cat)}">{escape(cat)}</button>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week of {date_str} - AI Academia Bot</title>
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <div class="container">
    <a href="../index.html" class="nav-back">&larr; Back to Archive</a>

    <h1>Week of {date_str}</h1>
    <div class="stats" style="justify-content:flex-start; margin: 1rem 0;">
      <div class="stat">
        <div class="stat-value">{len(papers)}</div>
        <div class="stat-label">Papers</div>
      </div>
      <div class="stat">
        <div class="stat-value">{ft50_count}</div>
        <div class="stat-label">FT50</div>
      </div>
      <div class="stat">
        <div class="stat-value">{utd24_count}</div>
        <div class="stat-label">UTD24</div>
      </div>
      <div class="stat">
        <div class="stat-value">{high_count}</div>
        <div class="stat-label">Innovation</div>
      </div>
    </div>

    <input type="text" class="search-box" placeholder="Search papers by title, author, or abstract..." id="searchBox">

    <div class="filters">
      {"".join(filter_btns)}
    </div>

    <div id="paperList">
      {"".join(sections)}
    </div>
  </div>

  <footer>
    Powered by <a href="https://openalex.org">OpenAlex</a> &middot;
    <a href="https://github.com/coujasmine/AI-academia-bot">GitHub</a>
  </footer>

  <script>
    // Category filter
    document.querySelectorAll('.filter-btn').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        document.querySelectorAll('.category-section').forEach(sec => {{
          sec.classList.toggle('hidden', filter !== 'all' && sec.dataset.category !== filter);
        }});
      }});
    }});

    // Search
    document.getElementById('searchBox').addEventListener('input', (e) => {{
      const q = e.target.value.toLowerCase();
      document.querySelectorAll('.paper-card').forEach(card => {{
        card.classList.toggle('hidden', q && !card.textContent.toLowerCase().includes(q));
      }});
    }});
  </script>
</body>
</html>"""

    (WEEK_DIR / f"{date_str}.html").write_text(html, encoding="utf-8")


def _render_paper_card(paper: dict) -> str:
    """Render a single paper as an HTML card."""
    title = escape(paper.get("title", "Untitled"))
    doi = paper.get("doi", "")
    url = doi or paper.get("url", "")
    authors = paper.get("authors", [])
    author_str = escape(", ".join(authors[:5]))
    if len(authors) > 5:
        author_str += f" ... (+{len(authors) - 5})"

    journal = escape(paper.get("journal_name", ""))
    abbr = escape(paper.get("journal_abbr", ""))
    pub_date = escape(paper.get("publication_date", ""))

    abstract = paper.get("abstract", "")
    if abstract:
        abstract = re.sub(r"<[^>]+>", "", abstract).strip()
        if len(abstract) > 400:
            abstract = abstract[:400] + "..."
        abstract_html = f'<p class="paper-abstract">{escape(abstract)}</p>'
    else:
        abstract_html = ""

    # Tags
    tags = []
    if paper.get("in_ft50"):
        tags.append('<span class="tag tag-ft50">FT50</span>')
    if paper.get("in_utd24"):
        tags.append('<span class="tag tag-utd24">UTD24</span>')
    rel = paper.get("innovation_relevance", "")
    if rel == "high":
        tags.append('<span class="tag tag-innovation">Innovation</span>')
    elif rel == "medium":
        tags.append('<span class="tag tag-medium">Related</span>')
    tags_html = f'<div class="tags">{"".join(tags)}</div>' if tags else ""

    title_html = f'<a href="{escape(url)}" target="_blank">{title}</a>' if url else title

    return f"""
      <div class="paper-card">
        <h3>{title_html}</h3>
        <p class="paper-meta">
          {journal} ({abbr}) &middot; {pub_date}
          {" &middot; " + author_str if author_str else ""}
        </p>
        {abstract_html}
        {tags_html}
      </div>"""


def _group_papers(papers: list[dict]) -> dict[str, list[dict]]:
    """Group papers by category in a predefined order."""
    from config.journals import JOURNALS

    grouped: dict[str, list[dict]] = {}
    for paper in papers:
        abbr = paper.get("journal_abbr", "")
        cat = "Other"
        for j in JOURNALS:
            if j["abbr"] == abbr:
                cat = j["category"]
                break
        grouped.setdefault(cat, []).append(paper)

    ordered = {}
    for cat in CATEGORY_ORDER:
        if cat in grouped:
            ordered[cat] = grouped.pop(cat)
    for cat in sorted(grouped.keys()):
        ordered[cat] = grouped[cat]
    return ordered
