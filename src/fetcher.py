"""
Paper fetcher using OpenAlex API (primary) and Crossref API (fallback).

OpenAlex is the recommended primary source because:
- Supports batch queries (up to 50 sources per request)
- Rich metadata including abstract inverted index
- Fully open (CC0 license)
- 100,000 requests/day rate limit
"""

import logging
import time
from datetime import datetime, timedelta

import requests

from config.journals import JOURNALS, get_journal_by_issn
from config.settings import (
    OPENALEX_BASE_URL,
    OPENALEX_EMAIL,
    CROSSREF_BASE_URL,
    CROSSREF_EMAIL,
    FETCH_DAYS,
)

logger = logging.getLogger(__name__)


# ── Helpers ────────────────────────────────────────────────────────────


def _reconstruct_abstract(inverted_index: dict | None) -> str:
    """Reconstruct abstract text from OpenAlex inverted index format.

    OpenAlex stores abstracts as {"word": [positions]} to save space.
    This function rebuilds the original text.
    """
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in word_positions)


def _openalex_headers() -> dict:
    """Build request headers for the OpenAlex polite pool."""
    headers = {"Accept": "application/json"}
    if OPENALEX_EMAIL:
        headers["User-Agent"] = f"AcademiaBot/1.0 (mailto:{OPENALEX_EMAIL})"
    return headers


def _crossref_headers() -> dict:
    """Build request headers for the Crossref polite pool."""
    headers = {"Accept": "application/json"}
    if CROSSREF_EMAIL:
        headers["User-Agent"] = f"AcademiaBot/1.0 (mailto:{CROSSREF_EMAIL})"
    return headers


# ── OpenAlex Source ID Resolution ──────────────────────────────────────


def resolve_openalex_source_ids(journals: list[dict]) -> dict:
    """Resolve OpenAlex source IDs for a list of journals using their ISSNs.

    Returns a mapping of journal abbr -> OpenAlex source ID (e.g. "S12345").
    """
    source_map = {}
    for journal in journals:
        for issn in journal["issn"]:
            try:
                resp = requests.get(
                    f"{OPENALEX_BASE_URL}/sources",
                    params={"filter": f"issn:{issn}"},
                    headers=_openalex_headers(),
                    timeout=30,
                )
                resp.raise_for_status()
                results = resp.json().get("results", [])
                if results:
                    source_id = results[0]["id"].replace("https://openalex.org/", "")
                    source_map[journal["abbr"]] = source_id
                    logger.info(
                        "Resolved %s (%s) -> %s",
                        journal["abbr"],
                        issn,
                        source_id,
                    )
                    break
            except requests.RequestException as e:
                logger.warning("Failed to resolve %s via ISSN %s: %s", journal["abbr"], issn, e)
            time.sleep(0.15)  # Respect rate limits
    return source_map


# ── OpenAlex Fetcher ──────────────────────────────────────────────────


def fetch_papers_openalex(
    journals: list[dict],
    days: int = FETCH_DAYS,
    source_ids: dict | None = None,
) -> list[dict]:
    """Fetch recent papers from OpenAlex for the given journals.

    Args:
        journals: List of journal dicts from config.journals
        days: Number of days to look back
        source_ids: Pre-resolved {abbr: source_id} mapping. If None,
                    falls back to ISSN-based filtering.

    Returns:
        List of paper dicts with normalized fields.
    """
    since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    papers = []

    if source_ids:
        # Batch query: OpenAlex supports up to 50 source IDs joined by |
        ids_str = "|".join(source_ids.values())
        _fetch_openalex_batch(ids_str, since, papers)
    else:
        # Fallback: query by ISSN one journal at a time
        for journal in journals:
            for issn in journal["issn"]:
                _fetch_openalex_by_issn(issn, since, papers)
                break  # One ISSN per journal is sufficient
            time.sleep(0.15)

    logger.info("OpenAlex: fetched %d papers total", len(papers))
    return papers


def _fetch_openalex_batch(source_ids_str: str, since: str, papers: list):
    """Fetch papers from OpenAlex using batched source IDs."""
    cursor = "*"
    while cursor:
        params = {
            "filter": f"primary_location.source.id:{source_ids_str},from_publication_date:{since}",
            "sort": "publication_date:desc",
            "per-page": 200,
            "cursor": cursor,
        }
        if OPENALEX_EMAIL:
            params["mailto"] = OPENALEX_EMAIL

        try:
            resp = requests.get(
                f"{OPENALEX_BASE_URL}/works",
                params=params,
                headers=_openalex_headers(),
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.error("OpenAlex batch query failed: %s", e)
            break

        for work in data.get("results", []):
            papers.append(_normalize_openalex_work(work))

        cursor = data.get("meta", {}).get("next_cursor")
        if not data.get("results"):
            break
        time.sleep(0.15)


def _fetch_openalex_by_issn(issn: str, since: str, papers: list):
    """Fetch papers from OpenAlex for a single ISSN."""
    params = {
        "filter": f"primary_location.source.issn:{issn},from_publication_date:{since}",
        "sort": "publication_date:desc",
        "per-page": 200,
    }
    if OPENALEX_EMAIL:
        params["mailto"] = OPENALEX_EMAIL

    try:
        resp = requests.get(
            f"{OPENALEX_BASE_URL}/works",
            params=params,
            headers=_openalex_headers(),
            timeout=30,
        )
        resp.raise_for_status()
        for work in resp.json().get("results", []):
            papers.append(_normalize_openalex_work(work))
    except requests.RequestException as e:
        logger.warning("OpenAlex query failed for ISSN %s: %s", issn, e)


def _normalize_openalex_work(work: dict) -> dict:
    """Normalize an OpenAlex work object into a standard paper dict."""
    # Extract journal info
    primary_loc = work.get("primary_location", {}) or {}
    source = primary_loc.get("source", {}) or {}
    issns = source.get("issn", []) or []

    # Try to match to our journal list
    journal_info = None
    for issn in issns:
        journal_info = get_journal_by_issn(issn)
        if journal_info:
            break

    # Authors
    authors = []
    for authorship in work.get("authorships", []):
        author = authorship.get("author", {}) or {}
        name = author.get("display_name", "")
        if name:
            authors.append(name)

    return {
        "title": work.get("title", ""),
        "authors": authors,
        "abstract": _reconstruct_abstract(work.get("abstract_inverted_index")),
        "journal_name": source.get("display_name", ""),
        "journal_abbr": journal_info["abbr"] if journal_info else "",
        "publication_date": work.get("publication_date", ""),
        "doi": work.get("doi", ""),
        "url": work.get("id", ""),
        "open_access": work.get("open_access", {}).get("is_oa", False),
        "cited_by_count": work.get("cited_by_count", 0),
        "topics": [
            t.get("display_name", "")
            for t in (work.get("topics", []) or [])[:5]
        ],
        "source": "openalex",
        "in_ft50": journal_info["in_ft50"] if journal_info else False,
        "in_utd24": journal_info["in_utd24"] if journal_info else False,
        "innovation_relevance": journal_info["innovation_relevance"] if journal_info else "unknown",
    }


# ── Crossref Fetcher (secondary) ─────────────────────────────────────


def fetch_papers_crossref(journals: list[dict], days: int = FETCH_DAYS) -> list[dict]:
    """Fetch recent papers from Crossref as a secondary/validation source.

    Crossref requires one query per ISSN (no batch support), so this is
    slower than OpenAlex but provides authoritative DOI metadata.
    """
    since = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    papers = []

    for journal in journals:
        issn = journal["issn"][0]  # Use primary ISSN
        try:
            resp = requests.get(
                f"{CROSSREF_BASE_URL}/journals/{issn}/works",
                params={
                    "filter": f"from-pub-date:{since}",
                    "sort": "published",
                    "order": "desc",
                    "rows": 50,
                    "select": "DOI,title,author,published,abstract,ISSN,container-title",
                },
                headers=_crossref_headers(),
                timeout=30,
            )
            resp.raise_for_status()
            items = resp.json().get("message", {}).get("items", [])
            for item in items:
                papers.append(_normalize_crossref_item(item, journal))
        except requests.RequestException as e:
            logger.warning("Crossref query failed for %s: %s", journal["abbr"], e)
        time.sleep(0.2)

    logger.info("Crossref: fetched %d papers total", len(papers))
    return papers


def _normalize_crossref_item(item: dict, journal: dict) -> dict:
    """Normalize a Crossref work item into a standard paper dict."""
    authors = []
    for author in item.get("author", []):
        given = author.get("given", "")
        family = author.get("family", "")
        name = f"{given} {family}".strip()
        if name:
            authors.append(name)

    # Parse publication date
    pub_date = ""
    date_parts = item.get("published", {}).get("date-parts", [[]])
    if date_parts and date_parts[0]:
        parts = date_parts[0]
        pub_date = "-".join(str(p).zfill(2) for p in parts)

    doi = item.get("DOI", "")

    return {
        "title": (item.get("title", [""]) or [""])[0],
        "authors": authors,
        "abstract": item.get("abstract", ""),
        "journal_name": journal["name"],
        "journal_abbr": journal["abbr"],
        "publication_date": pub_date,
        "doi": f"https://doi.org/{doi}" if doi else "",
        "url": f"https://doi.org/{doi}" if doi else "",
        "open_access": False,
        "cited_by_count": 0,
        "topics": [],
        "source": "crossref",
        "in_ft50": journal["in_ft50"],
        "in_utd24": journal["in_utd24"],
        "innovation_relevance": journal["innovation_relevance"],
    }


# ── Combined Fetch ────────────────────────────────────────────────────


def fetch_all_papers(
    journals: list[dict] | None = None,
    days: int = FETCH_DAYS,
    use_crossref: bool = False,
) -> list[dict]:
    """Fetch papers from all configured sources and deduplicate.

    Args:
        journals: Journals to query. Defaults to all configured journals.
        days: Number of days to look back.
        use_crossref: Also query Crossref for additional coverage.

    Returns:
        Deduplicated list of paper dicts, sorted by publication date (newest first).
    """
    if journals is None:
        journals = JOURNALS

    logger.info("Fetching papers from %d journals (last %d days)", len(journals), days)

    # Primary: OpenAlex
    papers = fetch_papers_openalex(journals, days=days)

    # Optional: Crossref
    if use_crossref:
        crossref_papers = fetch_papers_crossref(journals, days=days)
        papers = _deduplicate(papers, crossref_papers)

    # Sort by date descending
    papers.sort(key=lambda p: p.get("publication_date", ""), reverse=True)

    logger.info("Total unique papers: %d", len(papers))
    return papers


def _deduplicate(primary: list[dict], secondary: list[dict]) -> list[dict]:
    """Merge two paper lists, preferring primary source for duplicates."""
    seen_dois = set()
    seen_titles = set()
    result = []

    for paper in primary:
        doi = paper.get("doi", "").lower().strip()
        title = paper.get("title", "").lower().strip()
        if doi:
            seen_dois.add(doi)
        if title:
            seen_titles.add(title)
        result.append(paper)

    for paper in secondary:
        doi = paper.get("doi", "").lower().strip()
        title = paper.get("title", "").lower().strip()
        if doi and doi in seen_dois:
            continue
        if title and title in seen_titles:
            continue
        result.append(paper)

    return result
