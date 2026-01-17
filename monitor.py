import requests
from bs4 import BeautifulSoup
import os

# Configuration
URL = "https://holfuy.com/en/weather/1067"
THRESHOLD = 0.1 # Set low for testing!

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(speed):
    message = f"🌬️ Wind Alert! Station 1067 is reporting {speed}!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_weather():
    # We use a 'User-Agent' to pretend we are a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Since #j_speed is dynamic, we look for the 'og:description' tag 
    # which often contains the live weather summary in the metadata.
    meta_desc = soup.find("meta", property="og:description")
    
    if meta_desc:
        text = meta_desc["content"]
        print(f"Site Summary Found: {text}")
        
        # The text usually looks like: "Wind: 4.3 m/s, Temp: 12C..."
        # We extract the first number we find after 'Wind:'
        try:
            # Simple split to find the number near 'm/s'
            speed_part = text.split('m/s')[0].split(' ')[-1]
            current_speed = float(speed_part)
            print(f"Extracted Speed: {current_speed}")

            if current_speed > THRESHOLD:
                send_alert(current_speed)
        except Exception as e:
            print(f"Could not parse speed from text: {e}")
    else:
        print("Could not find weather metadata. Site might be blocking the script.")

if __name__ == "__main__":
    check_weather()
