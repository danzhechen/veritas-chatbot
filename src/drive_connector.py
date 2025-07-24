#!/usr/bin/env python3
"""
Google Drive Connector for Summer School Chatbot

This module handles all interactions with Google Drive API,
including authentication, document retrieval, and content extraction.
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

# Google Drive API imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Warning: Google Drive API dependencies not installed.")
    print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleDriveConnector:
    """Handles Google Drive API interactions for document retrieval."""
    
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    
    def __init__(self, credentials_file: str = None, folder_id: str = None):
        """
        Initialize the Google Drive connector.
        
        Args:
            credentials_file: Path to Google Drive API credentials
            folder_id: Google Drive folder ID to monitor
        """
        self.credentials_file = credentials_file or os.getenv('GOOGLE_DRIVE_CREDENTIALS_FILE')
        self.folder_id = folder_id or os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.service = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with Google Drive API."""
        creds = None
        
        # The file token.json stores the user's access and refresh tokens
        token_path = Path('config/token.json')
        
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), self.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not self.credentials_file:
                    logger.warning("No credentials file specified. Please set GOOGLE_DRIVE_CREDENTIALS_FILE")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            token_path.parent.mkdir(exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Successfully authenticated with Google Drive API")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Drive API: {e}")
    
    def list_documents(self, folder_id: str = None) -> List[Dict[str, Any]]:
        """
        List all documents in the specified folder.
        
        Args:
            folder_id: Google Drive folder ID (uses default if not provided)
            
        Returns:
            List of document metadata
        """
        if not self.service:
            logger.error("Google Drive service not initialized")
            return []
        
        folder_id = folder_id or self.folder_id
        if not folder_id:
            logger.error("No folder ID specified")
            return []
        
        try:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
            ).execute()
            
            documents = results.get('files', [])
            logger.info(f"Found {len(documents)} documents in folder")
            return documents
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return []
    
    def get_document_content(self, file_id: str) -> Optional[str]:
        """
        Retrieve the content of a specific document.
        
        Args:
            file_id: Google Drive file ID
            
        Returns:
            Document content as string, or None if error
        """
        if not self.service:
            logger.error("Google Drive service not initialized")
            return None
        
        try:
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id).execute()
            mime_type = file_metadata.get('mimeType', '')
            
            # Handle different file types
            if 'google-apps.document' in mime_type:
                return self._get_google_doc_content(file_id)
            elif 'text/plain' in mime_type or 'application/pdf' in mime_type:
                return self._get_file_content(file_id)
            else:
                logger.warning(f"Unsupported file type: {mime_type}")
                return None
                
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return None
    
    def _get_google_doc_content(self, file_id: str) -> Optional[str]:
        """Extract content from Google Docs."""
        try:
            document = self.service.files().export(
                fileId=file_id, 
                mimeType='text/plain'
            ).execute()
            return document.decode('utf-8')
        except Exception as e:
            logger.error(f"Error extracting Google Doc content: {e}")
            return None
    
    def _get_file_content(self, file_id: str) -> Optional[str]:
        """Download and extract content from regular files."""
        try:
            request = self.service.files().get_media(fileId=file_id)
            content = request.execute()
            return content.decode('utf-8')
        except Exception as e:
            logger.error(f"Error downloading file content: {e}")
            return None
    
    def search_documents(self, query: str, folder_id: str = None) -> List[Dict[str, Any]]:
        """
        Search for documents containing specific text.
        
        Args:
            query: Search query
            folder_id: Google Drive folder ID (uses default if not provided)
            
        Returns:
            List of matching documents
        """
        if not self.service:
            logger.error("Google Drive service not initialized")
            return []
        
        folder_id = folder_id or self.folder_id
        if not folder_id:
            logger.error("No folder ID specified")
            return []
        
        try:
            # Search for files containing the query
            results = self.service.files().list(
                q=f"'{folder_id}' in parents and trashed=false and fullText contains '{query}'",
                pageSize=50,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
            ).execute()
            
            documents = results.get('files', [])
            logger.info(f"Found {len(documents)} documents matching query: {query}")
            return documents
            
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return []
    
    def get_all_document_contents(self, folder_id: str = None) -> Dict[str, str]:
        """
        Retrieve content from all documents in the folder.
        
        Args:
            folder_id: Google Drive folder ID (uses default if not provided)
            
        Returns:
            Dictionary mapping document names to their content
        """
        documents = self.list_documents(folder_id)
        contents = {}
        
        for doc in documents:
            content = self.get_document_content(doc['id'])
            if content:
                contents[doc['name']] = content
        
        logger.info(f"Retrieved content from {len(contents)} documents")
        return contents

def main():
    """Test the Google Drive connector."""
    connector = GoogleDriveConnector()
    
    if connector.service:
        print("✅ Google Drive connector initialized successfully")
        
        # List documents
        documents = connector.list_documents()
        print(f"📁 Found {len(documents)} documents:")
        for doc in documents:
            print(f"  - {doc['name']} ({doc['mimeType']})")
    else:
        print("❌ Failed to initialize Google Drive connector")
        print("Please check your credentials and folder ID configuration")

if __name__ == "__main__":
    main() 