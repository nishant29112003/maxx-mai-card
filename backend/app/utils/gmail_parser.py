import os
import base64
from io import BytesIO
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PyPDF2 import PdfReader
from pymongo import MongoClient
from datetime import datetime
from app.config.config import MONGO_URI

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        CRED_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')
        flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
        
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def extract_pdf_text(service, msg_id):
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    for part in message['payload'].get('parts', []):
        if part['filename'].endswith('.pdf'):
            att_id = part['body']['attachmentId']
            att = service.users().messages().attachments().get(userId='me', messageId=msg_id, id=att_id).execute()
            data = base64.urlsafe_b64decode(att['data'])
            reader = PdfReader(BytesIO(data))
            return "\n".join(page.extract_text() for page in reader.pages)
    return None

def parse_and_store():
    service = authenticate_gmail()
    
    
    profile = service.users().getProfile(userId='me').execute()
    user_email = profile.get("emailAddress")

    results = service.users().messages().list(userId='me', maxResults=1, q='filename:pdf').execute()
    messages = results.get('messages', [])
    if not messages:
        print("No statement found.")
        return

    msg_id = messages[0]['id']
    text = extract_pdf_text(service, msg_id)
    
    if text:
        client = MongoClient(MONGO_URI)
        db = client['maxxcard']
        db.estatements.insert_one({
            "email_id": msg_id,
            "parsed_text": text,
            "timestamp": datetime.utcnow(),
            "user_email": user_email,        
            "preferences": None                
        })
