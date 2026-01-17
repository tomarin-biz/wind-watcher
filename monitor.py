import requests
import os

# Configuration
STATION_ID = "1067"
THRESHOLD = 1.0 # Set your wind speed threshold
URL = f"https://api.holfuy.com/live/?s={STATION_ID}&pw=FREE&m=JSON&tu=C&su=m/s"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(speed):
    message = f"🌬️ Wind Alert! Station 1067 is reporting {speed} m/s!"
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
    requests.get(api_url)

def check_weather():
    response = requests.get(URL)
    data = response.json()
    
    # Holfuy API returns wind speed in the 'windSpeed' field
    current_speed = float(data.get("windSpeed", 0))
    print(f"Current Wind Speed: {current_speed}")

    if current_speed > THRESHOLD:
        send_alert(current_speed)

if __name__ == "__main__":
    check_weather()
    
