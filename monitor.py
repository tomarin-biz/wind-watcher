import requests
from bs4 import BeautifulSoup
import os

# Configuration - Using the station info page
URL = "https://holfuy.com/en/station/1067"
THRESHOLD = 0.1 # Keep low for testing

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(speed):
    message = f"🌬️ Wind Alert! Station 1067 is reporting {speed} m/s!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(url)

def check_weather():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Website returned status {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We look for the 'td' (table cell) that contains 'm/s'
    # This page usually has a "Current Weather" table
    speed_cell = None
    for td in soup.find_all('td'):
        if 'm/s' in td.text:
            speed_cell = td.text
            break

    if speed_cell:
        print(f"Found speed data: {speed_cell}")
        try:
            # Extract only the numbers/decimal from the text
            clean_val = ''.join(c for c in speed_cell if c.isdigit() or c == '.')
            current_speed = float(clean_val)
            print(f"Success! Extracted Speed: {current_speed}")

            if current_speed > THRESHOLD:
                send_alert(current_speed)
        except Exception as e:
            print(f"Found data but couldn't parse: {e}")
    else:
        print("Could not find m/s in any table cell on this page.")

if __name__ == "__main__":
    check_weather()
