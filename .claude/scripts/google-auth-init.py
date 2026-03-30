#!/usr/bin/env python3
"""
Initialize Google OAuth authentication.
Run this once to get your refresh token.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate():
    credentials_file = '.google-credentials.json'
    token_file = '.google-token.json'

    if not os.path.exists(credentials_file):
        print(f"Error: {credentials_file} not found")
        print("Please download your OAuth credentials from Google Cloud Console and save as .google-credentials.json")
        return

    # Scopes needed for full Drive and Gmail access
    scopes = [
        'https://www.googleapis.com/auth/drive',  # Full Drive access
        'https://www.googleapis.com/auth/gmail.modify'  # Gmail read/write/delete
    ]

    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
    creds = flow.run_local_server(port=0)

    # Save the credentials
    with open(token_file, 'w') as f:
        f.write(creds.to_json())

    print(f"✓ Authentication successful!")
    print(f"✓ Token saved to {token_file}")
    print(f"✓ You can now use Google Drive and Gmail integrations")

if __name__ == '__main__':
    authenticate()
