import json
import imaplib
import email
from email.header import decode_header, make_header
import logging
from text_cleaner import clean_text
from config import USERNAME, PASSWORD, SERVER, MAILBOXES, EXTRACT_BATCH_SIZE

# Setup logging
logging.basicConfig(level=logging.INFO)

def decode_payload(payload, encoding):
    try:
        if encoding is None:
            return payload.decode('utf-8', errors='replace')
        return payload.decode(encoding, errors='replace')
    except (LookupError, UnicodeDecodeError):
        return payload.decode('utf-8', errors='replace')

def fetch_emails(mailbox, mail, email_ids):
    emails = []
    for email_id in email_ids:
        try:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode the subject and ensure it's a string
                    subject = msg.get('Subject')
                    if subject is not None:
                        subject = str(make_header(decode_header(subject)))
                    else:
                        subject = "(No Subject)"
                    
                    from_ = msg.get('From')
                    if from_ is not None:
                        from_ = str(make_header(decode_header(from_)))

                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get('Content-Disposition'))
                            try:
                                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                                    payload = part.get_payload(decode=True)
                                    body = decode_payload(payload, part.get_content_charset())
                                    break
                            except:
                                pass
                    else:
                        payload = msg.get_payload(decode=True)
                        body = decode_payload(payload, msg.get_content_charset())
                    
                    unique_id = f"{mailbox}_{email_id.decode()}"

                    email_data = {
                        'mailbox': mailbox,
                        "unique_id": unique_id,
                        'id': email_id.decode(),
                        'subject': subject,
                        'from': from_,
                        'has_attachment': any('attachment' in part.get('Content-Disposition') for part in msg.walk() if part.get('Content-Disposition') is not None),
                        'body': clean_text(body),
                    }
                    emails.append(email_data)
        except Exception as e:
            logging.error(f"Failed to fetch email ID {email_id} from mailbox {mailbox}: {e}")
    return emails

# Connect to the server
try:
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(USERNAME, PASSWORD)
except imaplib.IMAP4.error as e:
    logging.error(f"Failed to login: {e}")
    raise

all_emails = []

# Select the mailbox you want to use
for mailbox in MAILBOXES:
    try:
        mail.select(mailbox)
    except imaplib.IMAP4.error as e:
        logging.error(f"Failed to select mailbox {mailbox}: {e}")
        continue

    # Search for all emails in the mailbox
    status, messages = mail.search(None, 'ALL')
    if status != 'OK':
        logging.error(f"Failed to search emails in mailbox {mailbox}")
        continue

    # Convert the result list to a list of email IDs
    email_ids = messages[0].split()

    for i in range(0, len(email_ids), EXTRACT_BATCH_SIZE):
        batch = email_ids[i:i + EXTRACT_BATCH_SIZE]
        all_emails.extend(fetch_emails(mailbox, mail, batch))

mail.logout()

# Save the emails to a JSON file
with open('data/emails.json', 'w') as f:
    json.dump(all_emails, f)
