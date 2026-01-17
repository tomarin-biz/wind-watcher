import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL = "https://example.com"
THRESHOLD = 500
# These will be stored safely in GitHub Secrets
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(value):
    message = f"🚨 Alert! The number has reached {value}, which is above your threshold of {THRESHOLD}!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_site():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Update the selector to match your specific website element
    val_text = soup.select_one(".number-class").text
    current_val = float(val_text.replace(",", ""))

    if current_val > THRESHOLD:
        send_alert(current_val)

if __name__ == "__main__":
    check_site()
