#!/usr/bin/env python3
"""Google Drive operations - read, create, update, delete files and folders."""

import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleDrive:
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
                    ['https://www.googleapis.com/auth/drive']
                )
                creds = flow.run_local_server(port=0)

            with open(token_file, 'w') as f:
                f.write(creds.to_json())

        return build('drive', 'v3', credentials=creds)

    def list_files(self, folder_id=None, query=None):
        """List files in Drive or a specific folder"""
        q = query or ""
        if folder_id:
            q += f" and '{folder_id}' in parents"

        results = self.service.files().list(
            q=q,
            spaces='drive',
            pageSize=100,
            fields='files(id, name, mimeType, modifiedTime)'
        ).execute()
        return results.get('files', [])

    def get_file(self, file_id):
        """Get file metadata"""
        return self.service.files().get(fileId=file_id).execute()

    def create_file(self, name, content, mime_type='text/plain', folder_id=None):
        """Create a new file"""
        file_metadata = {'name': name}
        if folder_id:
            file_metadata['parents'] = [folder_id]

        file = self.service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(content, mimetype=mime_type)
        ).execute()
        return file

    def update_file(self, file_id, content):
        """Update file content"""
        self.service.files().update(
            fileId=file_id,
            media_body=MediaFileUpload(content)
        ).execute()

    def delete_file(self, file_id):
        """Delete a file"""
        self.service.files().delete(fileId=file_id).execute()

    def create_folder(self, name, parent_id=None):
        """Create a new folder"""
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        return folder

if __name__ == '__main__':
    drive = GoogleDrive()
    files = drive.list_files()
    print(json.dumps(files, indent=2))
