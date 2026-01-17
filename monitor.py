import requests
import os

# Configuration
STATION_ID = "1067"
THRESHOLD = 0.1  # Set to 0.1 JUST FOR TESTING so it triggers an alert
URL = f"https://api.holfuy.com/live/?s={STATION_ID}&pw=FREE&m=JSON&tu=C&su=m/s"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def check_weather():
    response = requests.get(URL)
    data = response.json()
    
    # DEBUG: This will show the full data in your GitHub logs
    print(f"Full API Response: {data}")

    # Holfuy API sometimes uses 'speed' instead of 'windSpeed'
    # We will try to find the speed in a few common places:
    speed = data.get("windSpeed") or data.get("speed") or 0
    
    current_speed = float(speed)
    print(f"Processed Wind Speed: {current_speed}")

    if current_speed > THRESHOLD:
        print("Threshold exceeded! Sending Telegram message...")
        message = f"🌬️ Wind Alert! Station 1067 is reporting {current_speed} m/s!"
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        res = requests.get(api_url)
        print(f"Telegram API Response: {res.status_code}")
    else:
        print("Speed is below threshold. No alert sent.")

if __name__ == "__main__":
    check_weather()
