"""
Report generator for weekly academic paper summaries.

Generates Markdown reports grouped by journal category, with optional
AI-powered summarization of abstracts.
"""

import logging
from datetime import datetime
from pathlib import Path

from config.settings import REPORTS_DIR, LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

logger = logging.getLogger(__name__)


def generate_report(
    papers: list[dict],
    title: str | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Generate a Markdown report from fetched papers.

    Args:
        papers: List of normalized paper dicts from fetcher.
        title: Report title. Defaults to "Weekly Academic Paper Summary".
        output_dir: Output directory. Defaults to REPORTS_DIR.

    Returns:
        Path to the generated report file.
    """
    if output_dir is None:
        output_dir = REPORTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    if title is None:
        title = f"Weekly Academic Paper Summary ({now.strftime('%Y-%m-%d')})"

    filename = f"report_{now.strftime('%Y%m%d_%H%M%S')}.md"
    filepath = output_dir / filename

    # Group papers by category
    grouped = _group_by_category(papers)

    # Build report content
    lines = []
    lines.append(f"# {title}\n")
    lines.append(f"**Generated:** {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"**Total papers:** {len(papers)}\n")

    # Summary stats
    ft50_count = sum(1 for p in papers if p.get("in_ft50"))
    utd24_count = sum(1 for p in papers if p.get("in_utd24"))
    high_rel = sum(1 for p in papers if p.get("innovation_relevance") == "high")
    lines.append(f"**FT50 papers:** {ft50_count} | **UTD24 papers:** {utd24_count} | **High innovation relevance:** {high_rel}\n")
    lines.append("---\n")

    # Table of contents
    lines.append("## Table of Contents\n")
    for cat in grouped:
        count = len(grouped[cat])
        anchor = cat.lower().replace(" ", "-").replace("&", "").replace("/", "")
        lines.append(f"- [{cat} ({count})](#{anchor})")
    lines.append("")

    # Paper sections
    for cat, cat_papers in grouped.items():
        lines.append(f"## {cat}\n")
        for i, paper in enumerate(cat_papers, 1):
            lines.append(_format_paper(paper, i))
        lines.append("")

    content = "\n".join(lines)
    filepath.write_text(content, encoding="utf-8")
    logger.info("Report generated: %s", filepath)
    return filepath


def _group_by_category(papers: list[dict]) -> dict[str, list[dict]]:
    """Group papers by journal category, with innovation-related categories first."""
    category_order = [
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
    grouped: dict[str, list[dict]] = {}
    for paper in papers:
        # Determine category from journal_abbr
        cat = _get_category(paper)
        grouped.setdefault(cat, []).append(paper)

    # Sort by predefined order
    ordered = {}
    for cat in category_order:
        if cat in grouped:
            ordered[cat] = grouped.pop(cat)
    # Add any remaining categories
    for cat in sorted(grouped.keys()):
        ordered[cat] = grouped[cat]
    return ordered


def _get_category(paper: dict) -> str:
    """Get the category for a paper based on its journal."""
    from config.journals import JOURNALS

    abbr = paper.get("journal_abbr", "")
    for j in JOURNALS:
        if j["abbr"] == abbr:
            return j["category"]
    return "Other"


def _format_paper(paper: dict, index: int) -> str:
    """Format a single paper as a Markdown section."""
    lines = []
    title = paper.get("title", "Untitled")
    doi = paper.get("doi", "")
    url = doi if doi else paper.get("url", "")

    # Title with link
    if url:
        lines.append(f"### {index}. [{title}]({url})\n")
    else:
        lines.append(f"### {index}. {title}\n")

    # Metadata
    authors = paper.get("authors", [])
    if authors:
        author_str = ", ".join(authors[:5])
        if len(authors) > 5:
            author_str += f" ... (+{len(authors) - 5} more)"
        lines.append(f"**Authors:** {author_str}\n")

    journal = paper.get("journal_name", "")
    abbr = paper.get("journal_abbr", "")
    pub_date = paper.get("publication_date", "")
    meta_parts = []
    if journal:
        meta_parts.append(f"**Journal:** {journal} ({abbr})")
    if pub_date:
        meta_parts.append(f"**Published:** {pub_date}")
    if paper.get("open_access"):
        meta_parts.append("**Open Access**")
    if meta_parts:
        lines.append(" | ".join(meta_parts) + "\n")

    # Tags
    tags = []
    if paper.get("in_ft50"):
        tags.append("`FT50`")
    if paper.get("in_utd24"):
        tags.append("`UTD24`")
    rel = paper.get("innovation_relevance", "")
    if rel == "high":
        tags.append("`Innovation-Core`")
    elif rel == "medium":
        tags.append("`Innovation-Related`")
    if tags:
        lines.append(" ".join(tags) + "\n")

    # Abstract
    abstract = paper.get("abstract", "")
    if abstract:
        # Clean up HTML tags that Crossref sometimes includes
        import re
        abstract = re.sub(r"<[^>]+>", "", abstract).strip()
        if len(abstract) > 800:
            abstract = abstract[:800] + "..."
        lines.append(f"> {abstract}\n")
    else:
        lines.append("> *Abstract not available*\n")

    # Topics
    topics = paper.get("topics", [])
    if topics:
        topic_str = ", ".join(topics)
        lines.append(f"**Topics:** {topic_str}\n")

    return "\n".join(lines)


# ── AI-Powered Summary (Optional) ────────────────────────────────────


def generate_ai_summary(papers: list[dict]) -> str:
    """Use an LLM to generate a high-level summary of this week's papers.

    Requires LLM_API_KEY to be configured. Returns empty string if not available.
    """
    if not LLM_API_KEY:
        logger.info("LLM_API_KEY not set, skipping AI summary")
        return ""

    try:
        import openai

        client = openai.OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    except ImportError:
        logger.warning("openai package not installed, skipping AI summary")
        return ""

    # Prepare paper summaries for the prompt
    paper_texts = []
    for p in papers[:30]:  # Limit to 30 papers to fit context
        text = f"- [{p.get('journal_abbr', '')}] {p.get('title', '')}"
        abstract = p.get("abstract", "")
        if abstract:
            text += f": {abstract[:200]}"
        paper_texts.append(text)

    prompt = f"""You are an academic research analyst specializing in management,
innovation, and entrepreneurship. Below is a list of recently published papers
from top management journals (FT50/UTD24).

Please provide:
1. A brief executive summary (2-3 paragraphs) of the key themes and trends
2. Highlight 3-5 papers most relevant to innovation and entrepreneurship research
3. Note any emerging research directions

Papers:
{chr(10).join(paper_texts)}

Please write in both English and Chinese (中英双语)."""

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error("AI summary generation failed: %s", e)
        return ""
