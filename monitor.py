import requests
from bs4 import BeautifulSoup
import os

# --- CONFIGURATION ---
URL = "https://holfuy.com/en/weather/1067"
THRESHOLD = 1  # <--- WRITE YOUR NUMBER HERE (No quotes)
# ---------------------

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(value):
    message = f"🚨 Alert! The value is {value}, which is above {THRESHOLD}!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_site():
    # Adding a 'User-Agent' makes you look like a real browser
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Use your copied selector here
    element = soup.select_one("#j_speed")
    
    if element:
        # This cleaning logic handles cases like "$1,250.00" -> 1250.0
        text_val = element.text.strip()
        numeric_val = float(''.join(c for c in text_val if c.isdigit() or c == '.'))

        print(f"Current Value found: {numeric_val}")

        if numeric_val > THRESHOLD:
            send_alert(numeric_val)
    else:
        print("Error: Could not find the number on the page.")

if __name__ == "__main__":
    check_site()
    
