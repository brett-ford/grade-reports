import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_credentials():
    """Returns credentials for accessing a Google account"""
    # Authenticate to Google API
    # Use one of the following scopes:
    #     'https://www.googleapis.com/auth/drive'
    #     'https://www.googleapis.com/auth/drive.file'
    #     'https://www.googleapis.com/auth/spreadsheets'
    # If modifying these scopes, delete token.pickle.
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive.file']

    credentials = None
    # The file token.pickle stores the user's access and refresh tokens.
    # token.pickle is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return credentials
