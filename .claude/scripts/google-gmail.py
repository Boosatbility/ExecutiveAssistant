#!/usr/bin/env python3
"""Gmail operations - read, create, update emails and drafts."""

import json
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleGmail:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        token_file = '.google-token.json'

        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '.google-credentials.json',
                    ['https://www.googleapis.com/auth/gmail.modify']
                )
                creds = flow.run_local_server(port=0)

            with open(token_file, 'w') as f:
                f.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def list_emails(self, query='', max_results=10):
        """List emails matching query"""
        results = self.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        return results.get('messages', [])

    def get_email(self, message_id):
        """Get full email content"""
        message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        return message

    def create_draft(self, to, subject, body, cc=None, bcc=None):
        """Create a draft email"""
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        message.attach(MIMEText(body, 'plain'))

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        draft = self.service.users().drafts().create(
            userId='me',
            body={'message': {'raw': raw}}
        ).execute()
        return draft

    def send_email(self, to, subject, body, cc=None, bcc=None):
        """Send an email"""
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc

        message.attach(MIMEText(body, 'plain'))

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        sent = self.service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        return sent

    def update_email(self, message_id, labels_to_add=None, labels_to_remove=None):
        """Update email labels"""
        self.service.users().messages().modify(
            userId='me',
            id=message_id,
            body={
                'addLabelIds': labels_to_add or [],
                'removeLabelIds': labels_to_remove or []
            }
        ).execute()

    def delete_email(self, message_id):
        """Delete an email"""
        self.service.users().messages().delete(
            userId='me',
            id=message_id
        ).execute()

if __name__ == '__main__':
    gmail = GoogleGmail()
    emails = gmail.list_emails(max_results=5)
    print(json.dumps(emails, indent=2))
