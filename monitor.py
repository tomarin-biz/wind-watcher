import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://holfuy.com/en/weather/1067"
THRESHOLD = 0.1  # Keep low for testing

def send_alert(speed):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    message = f"🌬️ Wind Alert! Station 1067 is reporting {speed} m/s!"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

def run():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Opening website...")
        page.goto(URL)
        
        # Wait for the specific element to load (up to 10 seconds)
        try:
            page.wait_for_selector("#j_speed", timeout=10000)
            speed_text = page.inner_text("#j_speed")
            print(f"Raw speed found: {speed_text}")
            
            # Clean and convert
            current_speed = float(''.join(c for c in speed_text if c.isdigit() or c == '.'))
            print(f"Success! Extracted Speed: {current_speed}")

            if current_speed > THRESHOLD:
                send_alert(current_speed)
                
        except Exception as e:
            print(f"Error finding speed: {e}")
            # Optional: save a screenshot to see what went wrong
            page.screenshot(path="error.png")
            
        browser.close()

if __name__ == "__main__":
    run()

