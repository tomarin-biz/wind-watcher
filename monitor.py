miimport os
import requests
from playwright.sync_api import sync_playwright

URL = "https://holfuy.com/en/weather/1067"
SPEED_THRESHOLD = 17.5  # Keep low for testing
GUST_THRESHOLD = 25
TENDENCY_THRESHOLD = 40

def send_alert(speed, gust, tendency):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    # Check for empty variables to avoid errors
    if not token or not chat_id:
        print("❌ Error: Missing Telegram Token or Chat ID in GitHub Secrets")
        return

    #message = f"**{speed}-{gust} kts of wind in the marina!**"
    message = f"""
🌬️ {speed}-{gust} kts of wind in the marina! The wind is {tendency}.
הרוח הגיעה ל {speed}-{gust} קשר במרינה!
    """
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # We send the data in a 'payload' dictionary
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    # Use .post() instead of .get()
    response = requests.post(url, json=payload)
    
    # This part is key: it tells us WHY it failed if it doesn't work
    if response.status_code == 200:
        print(f"✅ Alert sent successfully to {chat_id}")
    else:
        print(f"❌ Failed to send alert. Telegram said: {response.text}")

def run():
    with sync_playwright() as p:
        # Launch browser - we use chromium as it's the most reliable here
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(URL, wait_until="networkidle") # Wait until the page stops loading
            page.wait_for_selector("#j_speed", timeout=15000)
            speed_text = page.inner_text("#j_speed")
            gust_text = page.inner_text("#j_gust")
            tendency_text = page.inner_text("#j_speed_tend_str")
            
            print(tendency_text)
            if "%" in tendency_text: # Convert tendency percentage 
                tendency_number = float(percentage_str.replace("%", ""))
            else:  
                tendency_number = 0.0
            print(tendency_number)
            
            # Extract numbers
            current_speed = float(''.join(c for c in speed_text if c.isdigit() or c == '.'))
            current_gust = float(''.join(c for c in gust_text if c.isdigit() or c == '.'))

            if current_speed >= SPEED_THRESHOLD or current_gust >= GUST_THRESHOLD or tendency_number >= TENDENCY_THRESHOLD:
                send_alert(current_speed, current_gust, tendency_text)
                print(f"Alert sent for {current_speed}-{current_gust} kts")
            else:
                print(f"Checked: {current_speed} and {current_gust} kts are below thresholds and tendency is normal.")
                
        except Exception as e:
            print(f"Error during check: {e}")
            
        browser.close()

if __name__ == "__main__":
    run()

