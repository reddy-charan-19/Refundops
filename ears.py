import imaplib
import email
import time
import main

# --- CONFIGURATION ---
EMAIL_USER = "botpmail@gmail.com"
EMAIL_PASS = "ulnm ptka tcvw nshw"      
IMAP_SERVER = "imap.gmail.com"

def listen():
    print("👂 EARS: Connected to Gmail. Waiting for emails...", flush=True)
    while True:
        try:
            # 1. Connect
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(EMAIL_USER, EMAIL_PASS)
            mail.select("inbox")
            
            # 2. Search for UNSEEN (unread) emails (Gmail IMAP expects 'UNSEEN')
            status, messages = mail.search(None, 'UNSEEN')
            print(f"🔍 IMAP SEARCH status: {status}, messages: {messages}", flush=True)
            email_ids = messages[0].split()

            if email_ids:
                print(f"⚡ EARS: Found {len(email_ids)} new email(s)!", flush=True)
                
                for e_id in email_ids:
                    # Fetch content
                    _, msg_data = mail.fetch(e_id, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject = msg["Subject"]
                            
                            # Extract Body
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        print(f"📩 Subject: {subject}", flush=True)
                                        
                                        # 3. TRIGGER THE AGENT
                                        main.process_refund_email(body)
            
            # Sleep to prevent spamming Gmail
            time.sleep(5)

        except Exception as e:
            print(f"❌ Connection Error: {e}", flush=True)
            time.sleep(5)

if __name__ == "__main__":
    listen()