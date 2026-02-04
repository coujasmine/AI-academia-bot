#!/usr/bin/env python3
"""
AI Academia Bot - Weekly paper summary from FT50 & UTD24 journals.

Usage:
    python main.py --archive                 # Fetch & archive (last 60 days)
    python main.py --mode innovation --archive  # Innovation journals only
    python main.py --days 14 --archive       # Look back 14 days
    python main.py --crossref --archive      # Also query Crossref
"""

import argparse
import logging
import sys

from config.journals import get_journals, INNOVATION_TAGS
from config.settings import FETCH_DAYS, FILTER_MODE
from src.archive import ArchiveManager
from src.fetcher import fetch_all_papers
from src.report import generate_report, generate_ai_summary

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and summarize latest FT50/UTD24 papers"
    )
    parser.add_argument(
        "--mode",
        choices=["all", "innovation", "ft50", "utd24"],
        default=FILTER_MODE,
        help="Which journals to query (default: from FILTER_MODE env var)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=FETCH_DAYS,
        help=f"Days to look back (default: {FETCH_DAYS})",
    )
    parser.add_argument(
        "--crossref",
        action="store_true",
        help="Also query Crossref API for additional coverage",
    )
    parser.add_argument(
        "--ai-summary",
        action="store_true",
        help="Generate AI-powered summary (requires LLM_API_KEY)",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Archive report to archives/YYYY-MM-DD/ and update README index",
    )
    args = parser.parse_args()

    # Select journals based on mode
    if args.mode == "innovation":
        journals = get_journals(tags=INNOVATION_TAGS)
        logger.info("Mode: innovation-focused (%d journals)", len(journals))
    elif args.mode == "ft50":
        journals = get_journals(list_name="ft50")
        logger.info("Mode: FT50 (%d journals)", len(journals))
    elif args.mode == "utd24":
        journals = get_journals(list_name="utd24")
        logger.info("Mode: UTD24 (%d journals)", len(journals))
    else:
        journals = get_journals()
        logger.info("Mode: all journals (%d journals)", len(journals))

    # Fetch papers
    logger.info("Fetching papers from the last %d days...", args.days)
    papers = fetch_all_papers(
        journals=journals,
        days=args.days,
        use_crossref=args.crossref,
    )

    if not papers:
        logger.warning("No papers found for the given time range")
        print("No new papers found.")
        return

    logger.info("Found %d papers", len(papers))

    # Generate AI summary if requested
    ai_summary = ""
    if args.ai_summary:
        logger.info("Generating AI summary...")
        ai_summary = generate_ai_summary(papers)

    # Generate report
    report_path = generate_report(papers)
    logger.info("Report saved to: %s", report_path)

    # Append AI summary to report if available
    if ai_summary:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write("\n---\n\n## AI-Powered Weekly Summary\n\n")
            f.write(ai_summary)
            f.write("\n")
        logger.info("AI summary appended to report")

    # Archive to dated folder if requested
    if args.archive:
        logger.info("Archiving report...")
        archiver = ArchiveManager()
        archive_dir = archiver.save(papers, report_path)
        logger.info("Archived to: %s", archive_dir)

    # Print summary to console
    print(f"\n{'='*60}")
    print(f"Weekly Report Generated Successfully")
    print(f"{'='*60}")
    print(f"Total papers: {len(papers)}")
    print(f"FT50 papers:  {sum(1 for p in papers if p.get('in_ft50'))}")
    print(f"UTD24 papers: {sum(1 for p in papers if p.get('in_utd24'))}")
    print(f"Innovation-relevant: {sum(1 for p in papers if p.get('innovation_relevance') == 'high')}")
    print(f"Report: {report_path}")
    if args.archive:
        print(f"Archive: archives/{archiver.today}/")
    print(f"{'='*60}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
