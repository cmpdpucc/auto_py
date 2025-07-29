import asyncio
import os
from telethon import TelegramClient, events
from playwright.async_api import async_playwright
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# --- ⚙️ Configuration ---
# 1. Telegram Details
API_ID = 28043396  # Your API ID from my.telegram.org
API_HASH = 'f72340da2d054a1c226febf942637a87'
PHONE_NUMBER = '+447708479161'

# 2. Triggering Conditions (Configured for you)
TARGET_CHAT_ID = -1002359903313
AUTHORIZED_USERNAME = 'Kevin74660'

# 3. Email Notification Setup (You must fill this in)
# ⚠️ IMPORTANT: USE AN "APP PASSWORD", NOT YOUR REAL PASSWORD!
EMAIL_SENDER = 'dany.pu95@gmail.com'
EMAIL_PASSWORD = 'ecpl qaui koly fxsx'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_RECEIVER = 'dany.pu95@kakao.com'

# 4. Playwright Web Automation Details
AUTH_FILE = 'auth.json'
LOGIN_URL = 'https://txexss.com/h5/#/login'
TRADE_URL = 'https://txexss.com/h5/#/trade'
SCREENSHOT_FILE = "final_trade_result.png"

# --- 📧 Email Sending Function (Updated) ---
def send_report_email(signal_text, screenshot_path=None):
    """Sends an email with the signal text and attaches a screenshot if available."""
    print(f"📧 Preparing report email for {EMAIL_RECEIVER}...")
    try:
        msg = MIMEMultipart()
        msg['Subject'] = 'New Trading Signal Triggered'
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER

        # Attach the signal text as the email body
        msg.attach(MIMEText(signal_text, 'plain'))

        # Attach the screenshot if the path is valid
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screenshot_path))
                msg.attach(img)
            print("✅ Screenshot attached to email.")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("✅ Report email sent successfully!")
            
    except Exception as e:
        print(f"❌ Failed to send report email: {e}")

# --- 🤖 Web Automation Function (Updated) ---
async def execute_trade_flow():
    """
    Performs the browser automation and returns the path to the final screenshot.
    Returns None if it fails before taking the screenshot.
    """
    print("\n--- 🚀 Starting Browser Automation ---")
    screenshot_path = None
    if not os.path.exists(AUTH_FILE):
        print(f"❌ FATAL: Authentication file '{AUTH_FILE}' not found.")
        return None
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(storage_state=AUTH_FILE, **p.devices['iPhone 13'])
        page = await context.new_page()
        try:
            await page.goto(LOGIN_URL)
            await page.locator(".login-btn").click()
            await page.wait_for_url("https://txexss.com/h5/#/", timeout=10000)
            await page.goto(TRADE_URL)
            call_button_selector = ".btn.bg-success:has-text('CALL')"
            await page.locator(call_button_selector).wait_for(state='visible', timeout=10000)
            await page.locator(call_button_selector).click()
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"❌ An error occurred during the web flow: {e}")
        finally:
            print(f"📸 Taking screenshot and saving to '{SCREENSHOT_FILE}'...")
            await page.screenshot(path=SCREENSHOT_FILE)
            screenshot_path = SCREENSHOT_FILE
            await browser.close()
            print("--- ✅ Browser Automation Finished ---\n")
            return screenshot_path

# --- 📞 Telegram Client & Handler (Updated Logic) ---
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHAT_ID))
async def handler(event):
    """Listens for new messages and checks sender and content."""
    sender = await event.get_sender()
    sender_username = sender.username if sender else 'Unknown'
    message_text = event.message.message

    print(f"📬 New message from '{sender_username}'")

    if sender_username == AUTHORIZED_USERNAME:
        print("✅ Message is from the authorized user.")
        required_keys = ["Trading Type:", "Time Frame:", "Signal Time:", "Direction:", "Trading Quantity:"]
        if all(key in message_text for key in required_keys):
            print("✅ Message is a valid signal. Starting process...")
            
            # 1. Run the browser flow FIRST to get the screenshot
            screenshot_file_path = await execute_trade_flow()
            
            # 2. NOW send the email with both the text and the screenshot
            send_report_email(message_text, screenshot_file_path)
        else:
            print("-> Message from authorized user, but not a valid signal. Ignoring.")
    else:
        print(f"👤 Message ignored. Sender '{sender_username}' is not authorized.")

async def main():
    await client.start(PHONE_NUMBER)
    print("🤖 Bot is running and connected to Telegram.")
    print(f"👂 Listening for valid signals from '{AUTHORIZED_USERNAME}' in chat ID '{TARGET_CHAT_ID}'...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        print(f"CRITICAL: The authentication file '{AUTH_FILE}' does not exist.")
        print("Please run 'save_auth.py' to create it before starting the bot.")
    else:
        asyncio.run(main())