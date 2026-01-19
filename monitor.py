import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://holfuy.com/en/weather/1067"
THRESHOLD = 17.5  # Keep low for testing

def send_alert(speed):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Adding the link to the message
    message = (
        # f"🌬️ **Wind Alert!**\n"
        f"**{speed} kts of wind in the marina!**\n\n"
        # f"Check live data here: {URL}"
    )
    
    # We add parse_mode=Markdown so the bold text works
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=Markdown"
    requests.get(url)


def run():
    with sync_playwright() as p:
        # Launch browser - we use chromium as it's the most reliable here
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(URL, wait_until="networkidle") # Wait until the page stops loading
            page.wait_for_selector("#j_speed", timeout=15000)
            speed_text = page.inner_text("#j_speed")
            
            # Extract number
            current_speed = float(''.join(c for c in speed_text if c.isdigit() or c == '.'))

            if current_speed > THRESHOLD:
                send_alert(current_speed)
                print(f"Alert sent for {current_speed} knots")
            else:
                print(f"Checked: {current_speed} knots is below threshold.")
                
        except Exception as e:
            print(f"Error during check: {e}")
            
        browser.close()

if __name__ == "__main__":
    run()

