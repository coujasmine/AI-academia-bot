"""
Notification module for sending reports via email or webhook.
"""

import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

from config.settings import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    NOTIFY_EMAIL_TO,
    FEISHU_WEBHOOK_URL,
)

logger = logging.getLogger(__name__)


def send_email(subject: str, body: str, html: bool = False):
    """Send a notification email with the report.

    Args:
        subject: Email subject line.
        body: Email body content.
        html: Whether body is HTML (default: plain text / markdown).
    """
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, NOTIFY_EMAIL_TO]):
        logger.info("Email not configured, skipping email notification")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = NOTIFY_EMAIL_TO

    if html:
        msg.attach(MIMEText(body, "html", "utf-8"))
    else:
        msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, NOTIFY_EMAIL_TO.split(","), msg.as_string())
        logger.info("Email sent to %s", NOTIFY_EMAIL_TO)
    except Exception as e:
        logger.error("Failed to send email: %s", e)


def send_feishu(title: str, content: str):
    """Send a notification to Feishu/Lark via webhook.

    Args:
        title: Message title.
        content: Message content (plain text).
    """
    if not FEISHU_WEBHOOK_URL:
        logger.info("Feishu webhook not configured, skipping")
        return

    # Truncate if too long for Feishu
    if len(content) > 4000:
        content = content[:4000] + "\n\n... (truncated, see full report)"

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue",
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content,
                }
            ],
        },
    }

    try:
        resp = requests.post(
            FEISHU_WEBHOOK_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
        logger.info("Feishu notification sent")
    except requests.RequestException as e:
        logger.error("Failed to send Feishu notification: %s", e)


def notify_report(report_path: Path, papers_count: int):
    """Send notifications about the generated report.

    Args:
        report_path: Path to the generated report file.
        papers_count: Total number of papers in the report.
    """
    subject = f"📚 Weekly Academic Papers Summary - {papers_count} new papers"
    body = report_path.read_text(encoding="utf-8")

    send_email(subject, body)
    send_feishu(subject, body)
