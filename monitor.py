import requests
from bs4 import BeautifulSoup
import os

# Configuration - Using the WAP version of the site
URL = "https://holfuy.com/en/wap/1067"
THRESHOLD = 0.1 # Testing threshold

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(speed):
    message = f"🌬️ Wind Alert! Station 1067 is reporting {speed} m/s!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_weather():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    
    # This site is very simple HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # The WAP site lists data in bold tags or plain text. 
    # We'll look for the string that contains "m/s"
    page_text = soup.get_text()
    print(f"Page Content: {page_text}") # For debugging

    if "m/s" in page_text:
        try:
            # Logic: Find 'm/s', look at the text immediately before it
            parts = page_text.split("m/s")[0].strip().split()
            current_speed = float(parts[-1])
            print(f"Success! Extracted Speed: {current_speed}")

            if current_speed > THRESHOLD:
                send_alert(current_speed)
        except Exception as e:
            print(f"Found m/s but couldn't parse number: {e}")
    else:
        print("Still couldn't find the wind speed on the page.")

if __name__ == "__main__":
    check_weather()
