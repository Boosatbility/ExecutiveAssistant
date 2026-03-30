#!/usr/bin/env python3
"""
Create a Gmail draft with meeting summary and action items.

Usage:
    python3 create_draft.py \
        --to "recipient@example.com" \
        --subject "Meeting summary: <topic>" \
        --body "Email body text"

Auth:
    First-time: runs OAuth flow, saves token to ~/.gmail_token.json
    Credentials file: ~/.gmail_credentials.json (download from Google Cloud Console)
"""

import argparse
import base64
import json
import os
import sys
from email.mime.text import MIMEText
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".gmail_credentials.json"
TOKEN_FILE = Path.home() / ".gmail_token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def get_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: Gmail credentials not found at {CREDENTIALS_FILE}")
                print()
                print("Setup steps:")
                print("  1. Go to https://console.cloud.google.com/")
                print("  2. Create a project (or select existing)")
                print("  3. Enable Gmail API")
                print("  4. Create OAuth 2.0 credentials (Desktop app)")
                print(f"  5. Download as {CREDENTIALS_FILE}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    return creds


def create_draft(to_addresses, subject, body):
    from googleapiclient.discovery import build

    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body, "plain")
    message["to"] = ", ".join(to_addresses) if isinstance(to_addresses, list) else to_addresses
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()

    print(f"Draft created: {draft['id']}")
    print(f"To: {message['to']}")
    print(f"Subject: {subject}")
    return draft


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Gmail draft")
    parser.add_argument("--to", required=True, help="Recipient email(s), comma-separated")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Email body text")
    args = parser.parse_args()

    to_list = [e.strip() for e in args.to.split(",")]
    create_draft(to_list, args.subject, args.body)
