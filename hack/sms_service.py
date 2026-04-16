import webbrowser
import urllib.parse
from config import CAMERAS

def send_sms(to_number, message_body=None):
    if not message_body:
        message_body = f"stampede risk at {CAMERAS[0]['id']} location"
        
    encoded_message = urllib.parse.quote(message_body)
    
    # We use WhatsApp via web API so it opens Desktop WhatsApp or Web WhatsApp smoothly
    # For default mobile SMS you could also use f"sms:{to_number}?body={encoded_message}"
    url = f"https://api.whatsapp.com/send?phone={to_number}&text={encoded_message}"
    
    print("=="*20)
    print(f"[MESSAGING NOTIFICATION]")
    print(f"To: {to_number}")
    print(f"Message: {message_body}")
    print("Opening WhatsApp client...")
    print("=="*20)
    
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Failed to open browser: {e}")
        return False
