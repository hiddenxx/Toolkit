#!/usr/bin/env python
from __future__ import print_function
import logger
import pickle
import os.path
import menu
import pydrive
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import *

logger = logger.get_logger(__name__)
MimeType = {"folders":"application/vnd.google-apps.folder","images":"image/jpeg",
            "spreadsheet":"application/vnd.google-apps.spreadsheet","text":"text/plain"}

class Toolkit(pydrive):
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.service = None
        self.response = None
        self.page_token = None
        self.file_path = None

    def google_drive_authenticator(self):
        # If modifying these scopes, delete the file token.pickle.
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        logger.info("Initializing Authentication Process.")
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)
        logger.info("Authentication Process completed.")
        return self.service


    def google_drive_rootUpdate(self):
        self.response = self.service.files().list().execute()
        self.google_drive_printer()

    def google_drive_uploader(self):
        logger.info("Starting Drive Uploader.")
        if not self.file_path:
            self.file_path = input("Please input the file path or Drag and Drop the file into the Console.")

        logger.info(f"{os.path.basename(self.file_path)} is in {self.file_path}")
        file_metadata = {'name': os.path.basename(self.file_path)}
        media = MediaFileUpload(os.path.basename(self.file_path))
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id,name,mimeType').execute()
        logger.info(f"File Name: {file.get('name')} File ID: {file.get('id')} MimeType: {file.get('mimeType')} - Uploaded.")
        if not file:
            print(f"{os.path.basename} Upload failed.", sep=' ', end='n', file=sys.stdout, flush=False)
            logger.info(f"{os.path.basename} Upload Failed.")
        # logger.info(f"Starting a Query for {q}")
        # self.response = self.service.files().list(q=f"mimeType='{MimeType[q]}'",
        #                                   spaces='drive',
        #                                   fields='nextPageToken, files(id, name)',
        #                                   pageToken=self.page_token).execute()

        return self.response

    def google_drive_printer(self):
        for file in self.response.get('files', []):
                # Process change
            print ('Found file: %s (%s)' % (file.get('name'), (file.get('id'))))
            self.page_token = self.response.get('nextPageToken', None)
            if self.page_token is None:
                break

def Return():
    return

def Exit():
    print("\n\tThanks for using my program!\n")

if __name__ == '__main__':
    mmObj = menu.Menu()
    mmObj.setPrompt("Select an Option\n")

    googleMenu = menu.Menu()
    googleObj = Toolkit()
    googleMenu.setPrompt("Select an Option\n")
    googleMenu.addOption(1,"Google Drive File Uploader",googleObj.google_drive_uploader,False)
    googleMenu.addOption(2,"Google Drive Root Updater",googleObj.google_drive_rootUpdate,False)
    googleMenu.addOption(3,"Return",Return,True)

    mmObj.addOption(1,"Google Drive Toolkit",googleMenu,False)
    mmObj.addOption(2,"Exit",Exit,True)
    mmObj.run()
