"""
Static site generator for GitHub Pages.

Reads archived paper data (archives/*/data.json) and generates a set of
static HTML pages under docs/ that can be served by GitHub Pages.

Pages generated:
  - docs/index.html              Main page with week list and aggregate stats
  - docs/week/YYYY-MM-DD.html    Detail page for each weekly archive
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

CATEGORY_COLORS = {
    "Entrepreneurship": "entre",
    "Innovation & Technology Policy": "innov",
    "Management": "mgmt",
    "Strategy": "strategy",
    "Organization": "org",
    "Management Science": "mgmt",
    "International Business": "mgmt",
    "Practitioner": "mgmt",
    "Marketing": "mktg",
    "Information Systems": "is",
    "Operations Management": "ops",
    "Operations Research": "ops",
    "OB & HR": "hr",
    "Accounting": "acct",
    "Finance": "fin",
    "Economics": "econ",
    "Ethics": "ethics",
}


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
    total_ft50 = sum(sum(1 for p in papers if p.get("in_ft50")) for papers in weeks.values())
    total_innov = sum(sum(1 for p in papers if p.get("innovation_relevance") == "high") for papers in weeks.values())

    week_rows = []
    for date_str, papers in weeks.items():
        ft50 = sum(1 for p in papers if p.get("in_ft50"))
        utd24 = sum(1 for p in papers if p.get("in_utd24"))
        high = sum(1 for p in papers if p.get("innovation_relevance") == "high")
        week_rows.append(f"""
      <li class="week-item">
        <div>
          <a href="week/{date_str}.html">Week of {date_str}</a>
        </div>
        <div class="week-meta">
          {len(papers)} papers · FT50: {ft50} · UTD24: {utd24} · Innovation: {high}
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
  <header class="header">
    <div class="header-content">
      <div class="header-icon">📚</div>
      <h1>AI Academia Bot</h1>
      <p class="header-subtitle">FT50 & UTD24 Weekly Paper Archive · Management, Innovation & Entrepreneurship</p>
    </div>
  </header>

  <div class="stats-bar">
    <div class="stats-grid">
      <div class="stat-item">
        <div class="stat-number">{total_weeks}</div>
        <div class="stat-label">Weeks</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{total_papers}</div>
        <div class="stat-label">Papers</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{total_ft50}</div>
        <div class="stat-label">FT50</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{total_innov}</div>
        <div class="stat-label">Innovation</div>
      </div>
    </div>
  </div>

  <main class="main">
    <ul class="week-list">
      {"".join(week_rows)}
    </ul>
  </main>

  <footer class="footer">
    Powered by <a href="https://openalex.org">OpenAlex</a> ·
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
    medium_count = sum(1 for p in papers if p.get("innovation_relevance") == "medium")

    sections = []
    paper_idx = 0
    for cat, cat_papers in grouped.items():
        color_key = CATEGORY_COLORS.get(cat, "mgmt")
        cards = []
        for p in cat_papers:
            paper_idx += 1
            cards.append(_render_paper_card(p, paper_idx))
        sections.append(f"""
    <section class="category-section" data-category="{escape(cat)}">
      <div class="category-header">
        <span class="category-dot" style="background: var(--category-{color_key})"></span>
        <h2>{escape(cat)}</h2>
        <span class="category-count">{len(cat_papers)} papers</span>
      </div>
      {"".join(cards)}
    </section>""")

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
  <header class="header">
    <div class="header-content">
      <div class="header-icon">📄</div>
      <h1>Weekly Paper Summary</h1>
      <p class="header-date">{date_str}</p>
      <p class="header-subtitle">FT50 & UTD24 · Management, Innovation & Entrepreneurship</p>
    </div>
  </header>

  <div class="stats-bar">
    <div class="stats-grid">
      <div class="stat-item">
        <div class="stat-number">{len(papers)}</div>
        <div class="stat-label">Papers</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{ft50_count}</div>
        <div class="stat-label">FT50</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{utd24_count}</div>
        <div class="stat-label">UTD24</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{high_count}</div>
        <div class="stat-label">Innovation</div>
      </div>
    </div>
  </div>

  <main class="main">
    <a href="../index.html" class="nav-back">← Back to Archive</a>

    <input type="text" class="search-box" placeholder="Search papers by title, author, journal, or abstract..." id="searchBox">

    <div class="filters">
      {"".join(filter_btns)}
    </div>

    <div id="paperList">
      {"".join(sections)}
    </div>
  </main>

  <footer class="footer">
    Powered by <a href="https://openalex.org">OpenAlex</a> ·
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


def _render_paper_card(paper: dict, idx: int = 0) -> str:
    """Render a single paper as an HTML card with premium design."""
    title = escape(paper.get("title", "Untitled"))
    doi = paper.get("doi", "")
    url = doi or paper.get("url", "")
    authors = paper.get("authors", [])
    author_str = escape(", ".join(authors[:4]))
    if len(authors) > 4:
        author_str += f" (+{len(authors) - 4} more)"

    journal = escape(paper.get("journal_name", ""))
    abbr = escape(paper.get("journal_abbr", ""))
    pub_date = escape(paper.get("publication_date", ""))

    # Abstract section
    abstract = paper.get("abstract", "")
    if abstract:
        abstract = re.sub(r"<[^>]+>", "", abstract).strip()
        if len(abstract) > 500:
            abstract = abstract[:500] + "..."
        abstract_html = f'''
        <div class="paper-abstract">
          <div class="abstract-label">Abstract</div>
          <p class="abstract-text">{escape(abstract)}</p>
        </div>'''
    else:
        abstract_html = ""

    # Tags section
    tags = []
    if paper.get("in_ft50"):
        tags.append('<span class="tag tag-ft50">FT50</span>')
    if paper.get("in_utd24"):
        tags.append('<span class="tag tag-utd24">UTD24</span>')
    rel = paper.get("innovation_relevance", "")
    if rel == "high":
        tags.append('<span class="tag tag-innovation">Innovation-Core</span>')
    elif rel == "medium":
        tags.append('<span class="tag tag-medium">Innovation-Related</span>')
    tags_html = f'''
        <div class="paper-tags">
          {"".join(tags)}
        </div>''' if tags else ""

    # Topics section
    topics = paper.get("topics", [])
    if topics:
        topic_chips = "".join(f'<span class="topic-chip">{escape(t)}</span>' for t in topics[:5])
        topics_html = f'''
        <div class="paper-topics">
          <span class="topics-label">Topics</span>
          {topic_chips}
        </div>'''
    else:
        topics_html = ""

    title_html = f'<a href="{escape(url)}" target="_blank" rel="noopener">{title}</a>' if url else title

    # DOI display
    doi_display = ""
    if doi and doi.startswith("https://doi.org/"):
        doi_id = doi.replace("https://doi.org/", "")
        doi_display = f'<a href="{escape(doi)}" target="_blank" rel="noopener">{escape(doi_id)}</a>'

    return f"""
      <article class="paper-card">
        <div class="paper-title-bar">
          <div class="paper-index">Paper #{idx:02d}</div>
          <h3 class="paper-title">{title_html}</h3>
        </div>
        <div class="paper-meta">
          <div class="meta-item">
            <span class="meta-label">Journal</span>
            <span class="meta-value journal">{journal} ({abbr})</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Published</span>
            <span class="meta-value">{pub_date}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Authors</span>
            <span class="meta-value">{author_str if author_str else "—"}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">DOI</span>
            <span class="meta-value">{doi_display if doi_display else "—"}</span>
          </div>
        </div>
        {tags_html}
        {abstract_html}
        {topics_html}
      </article>"""


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
