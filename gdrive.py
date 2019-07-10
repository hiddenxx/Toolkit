#!/usr/bin/env python
from __future__ import print_function
import logger
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


logger = logger.get_logger(__name__)
MimeType = {"folders":"application/vnd.google-apps.folder","images":"image/jpeg"}
class GoogleUploader():
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.service = None
        self.response = None
        self.page_token = None

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

        # # Call the Drive v3 API
        # results = service.files().list(fields="nextPageToken, files(id, name)").execute()
        # items = results.get('files', [])
        #
        # if not items:
        #     print('No files found.')
        # else:
        #     print('Files:')
        #     for item in items:
        #         print(u'{0} ({1})'.format(item['name'], item['id']))
    def service_driver(self,q):
        # A Service driver for different Mime Types and Uploaders and Fetchers will be here.
        # Mimetype is used to identify the folder or file.
        # Spaces is where it checks.
        # Fields nextpagetoken is required to go till EOF searching.
        # Files(id,name) is used to get the file ID and Name.
        logger.info(f"Starting a Query for {q}")
        self.response = self.service.files().list(q=f"mimeType='{MimeType[q]}'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=self.page_token).execute()
        return self.response

    def google_drive_printer(self,response):
        for file in response.get('files', []):
                # Process change
            print ('Found file: %s (%s)' % (file.get('name'), (file.get('id'))))
            page_token = response.get('nextPageToken', None)
            if self.page_token is None:
                break

if __name__ == '__main__':
    googleObj = GoogleUploader()
    googleObj.google_drive_authenticator()
    googleObj.google_drive_printer(googleObj.service_driver("folders"))
