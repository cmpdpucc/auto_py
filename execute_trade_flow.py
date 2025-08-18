# # import asyncio
# # import os
# # from telethon import TelegramClient, events
# # from playwright.async_api import async_playwright
# # import smtplib
# # from email.mime.multipart import MIMEMultipart
# # from email.mime.text import MIMEText
# # from email.mime.image import MIMEImage

# # # --- ⚙️ Configuration ---
# # # 1. Telegram Details
# # API_ID = 23609872  # Your API ID from my.telegram.org
# # API_HASH = '6d8206f84181146efb9f9a636d5321eb'
# # PHONE_NUMBER = '+393505183610'

# # # 2. Triggering Conditions (Configured for you)
# # TARGET_CHAT_ID = -1002359903313
# # AUTHORIZED_USERNAME = 'Pesc'

# # # 3. Email Notification Setup (You must fill this in)
# # # ⚠️ IMPORTANT: USE AN "APP PASSWORD", NOT YOUR REAL PASSWORD!
# # EMAIL_SENDER = 'dany.pu95@gmail.com'
# # EMAIL_PASSWORD = 'ecpl qaui koly fxsx'
# # SMTP_SERVER = 'smtp.gmail.com'
# # SMTP_PORT = 587
# # EMAIL_RECEIVER = 'dany.pu95@kakao.com'

# # # 4. Playwright Web Automation Details
# # AUTH_FILE = 'auth.json'
# # LOGIN_URL = 'https://txexss.com/h5/#/login'
# # TRADE_URL = 'https://txexss.com/h5/#/trade'
# # SCREENSHOT_FILE = "final_trade_result.png"

# # # --- 📧 Email Sending Function (Updated) ---
# # def send_report_email(signal_text, screenshot_path=None):
# #     """Sends an email with the signal text and attaches a screenshot if available."""
# #     print(f"📧 Preparing report email for {EMAIL_RECEIVER}...")
# #     try:
# #         msg = MIMEMultipart()
# #         msg['Subject'] = 'New Trading Signal Triggered'
# #         msg['From'] = EMAIL_SENDER
# #         msg['To'] = EMAIL_RECEIVER

# #         # Attach the signal text as the email body
# #         msg.attach(MIMEText(signal_text, 'plain'))

# #         # Attach the screenshot if the path is valid
# #         if screenshot_path and os.path.exists(screenshot_path):
# #             with open(screenshot_path, 'rb') as f:
# #                 img = MIMEImage(f.read())
# #                 img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screenshot_path))
# #                 msg.attach(img)
# #             print("✅ Screenshot attached to email.")
        
# #         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
# #             server.starttls()
# #             server.login(EMAIL_SENDER, EMAIL_PASSWORD)
# #             server.send_message(msg)
# #             print("✅ Report email sent successfully!")
            
# #     except Exception as e:
# #         print(f"❌ Failed to send report email: {e}")

# # # --- 🤖 Web Automation Function (Updated) ---
# # async def execute_trade_flow():
# #     """
# #     Performs the browser automation and returns the path to the final screenshot.
# #     Returns None if it fails before taking the screenshot.
# #     """
# #     print("\n--- 🚀 Starting Browser Automation ---")
# #     screenshot_path = None
# #     if not os.path.exists(AUTH_FILE):
# #         print(f"❌ FATAL: Authentication file '{AUTH_FILE}' not found.")
# #         return None
        
# #     async with async_playwright() as p:
# #         browser = await p.chromium.launch(headless=False, slow_mo=500)
# #         context = await browser.new_context(storage_state=AUTH_FILE, **p.devices['iPhone 13'])
# #         page = await context.new_page()
# #         try:
# #             await page.goto(LOGIN_URL)
# #             await page.locator(".login-btn").click()
# #             await page.wait_for_url("https://txexss.com/h5/#/", timeout=10000)
# #             await page.goto(TRADE_URL)
# #             call_button_selector = ".btn.bg-success:has-text('CALL')"
# #             await page.locator(call_button_selector).wait_for(state='visible', timeout=10000)
# #             await page.locator(call_button_selector).click()
# #             await page.wait_for_timeout(3000)
# #         except Exception as e:
# #             print(f"❌ An error occurred during the web flow: {e}")
# #         finally:
# #             print(f"📸 Taking screenshot and saving to '{SCREENSHOT_FILE}'...")
# #             await page.screenshot(path=SCREENSHOT_FILE)
# #             screenshot_path = SCREENSHOT_FILE
# #             await browser.close()
# #             print("--- ✅ Browser Automation Finished ---\n")
# #             return screenshot_path

# # # --- 📞 Telegram Client & Handler (Updated Logic) ---
# # client = TelegramClient('bot_session', API_ID, API_HASH)

# # @client.on(events.NewMessage(chats=TARGET_CHAT_ID))
# # async def handler(event):
# #     """Listens for new messages and checks sender and content."""
# #     sender = await event.get_sender()
# #     sender_username = sender.username if sender else 'Unknown'
# #     message_text = event.message.message

# #     print(f"📬 New message from '{sender_username}'")

# #     if sender_username == AUTHORIZED_USERNAME:
# #         print("✅ Message is from the authorized user.")
# #         required_keys = ["Trading Type:", "Time Frame:", "Signal Time:", "Direction:", "Trading Quantity:"]
# #         if all(key in message_text for key in required_keys):
# #             print("✅ Message is a valid signal. Starting process...")
            
# #             # 1. Run the browser flow FIRST to get the screenshot
# #             screenshot_file_path = await execute_trade_flow()
            
# #             # 2. NOW send the email with both the text and the screenshot
# #             send_report_email(message_text, screenshot_file_path)
# #         else:
# #             print("-> Message from authorized user, but not a valid signal. Ignoring.")
# #     else:
# #         print(f"👤 Message ignored. Sender '{sender_username}' is not authorized.")

# # async def main():
# #     await client.start(PHONE_NUMBER)
# #     print("🤖 Bot is running and connected to Telegram.")
# #     print(f"👂 Listening for valid signals from '{AUTHORIZED_USERNAME}' in chat ID '{TARGET_CHAT_ID}'...")
# #     await client.run_until_disconnected()

# # if __name__ == "__main__":
# #     if not os.path.exists(AUTH_FILE):
# #         print(f"CRITICAL: The authentication file '{AUTH_FILE}' does not exist.")
# #         print("Please run 'save_auth.py' to create it before starting the bot.")
# #     else:
# #         asyncio.run(main())


# import asyncio
# import os
# from telethon import TelegramClient, events
# from playwright.async_api import async_playwright
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage

# # --- ⚙️ Configuration ---
# # 1. Telegram Details
# API_ID = 23609872  # Your API ID from my.telegram.org
# API_HASH = '6d8206f84181146efb9f9a636d5321eb'
# PHONE_NUMBER = '+393505183610'

# # 2. Triggering Conditions (Updated for you)
# TARGET_CHAT_ID = -1002359903313
# # ⬇️ INSERISCI QUI IL TUO USER ID NUMERICO ⬇️
# AUTHORIZED_USER_ID = 6765291471  

# # 3. Email Notification Setup (You must fill this in)
# EMAIL_SENDER = 'your-sender-email@gmail.com'
# EMAIL_PASSWORD = 'YOUR_16_DIGIT_APP_PASSWORD'
# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 587
# EMAIL_RECEIVER = 'dany.pu95@kakao.com'

# # 4. Playwright Web Automation Details
# AUTH_FILE = 'auth.json'
# LOGIN_URL = 'https://txexss.com/h5/#/login'
# TRADE_URL = 'https://txexss.com/h5/#/trade'
# SCREENSHOT_FILE = "final_trade_result.png"

# # --- 📧 Email Sending Function ---
# def send_report_email(signal_text, screenshot_path=None):
#     """Sends an email with the signal text and attaches a screenshot if available."""
#     print(f"📧 Preparing report email for {EMAIL_RECEIVER}...")
#     try:
#         msg = MIMEMultipart()
#         msg['Subject'] = 'New Trading Signal Triggered'
#         msg['From'] = EMAIL_SENDER
#         msg['To'] = EMAIL_RECEIVER
#         msg.attach(MIMEText(signal_text, 'plain'))
#         if screenshot_path and os.path.exists(screenshot_path):
#             with open(screenshot_path, 'rb') as f:
#                 img = MIMEImage(f.read())
#                 img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screenshot_path))
#                 msg.attach(img)
#             print("✅ Screenshot attached to email.")
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls()
#             server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#             server.send_message(msg)
#             print("✅ Report email sent successfully!")
#     except Exception as e:
#         print(f"❌ Failed to send report email: {e}")

# # --- 🤖 Web Automation Function ---
# async def execute_trade_flow():
#     """Performs the browser automation and returns the path to the final screenshot."""
#     print("\n--- 🚀 Starting Browser Automation ---")
#     screenshot_path = None
#     if not os.path.exists(AUTH_FILE):
#         print(f"❌ FATAL: Authentication file '{AUTH_FILE}' not found.")
#         return None
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False, slow_mo=500)
#         context = await browser.new_context(storage_state=AUTH_FILE, **p.devices['iPhone 13'])
#         page = await context.new_page()
#         try:
#             await page.goto(LOGIN_URL)
#             await page.locator(".login-btn").click()
#             await page.wait_for_url("https://txexss.com/h5/#/", timeout=10000)
#             await page.goto(TRADE_URL)
#             call_button_selector = ".btn.bg-success:has-text('CALL')"
#             await page.locator(call_button_selector).wait_for(state='visible', timeout=10000)
#             await page.locator(call_button_selector).click()
#             await page.wait_for_timeout(3000)
#         except Exception as e:
#             print(f"❌ An error occurred during the web flow: {e}")
#         finally:
#             print(f"📸 Taking screenshot and saving to '{SCREENSHOT_FILE}'...")
#             await page.screenshot(path=SCREENSHOT_FILE)
#             screenshot_path = SCREENSHOT_FILE
#             await browser.close()
#             print("--- ✅ Browser Automation Finished ---\n")
#             return screenshot_path

# # --- 📞 Telegram Client & Handler (Updated Logic) ---
# client = TelegramClient('bot_session', API_ID, API_HASH)

# @client.on(events.NewMessage(chats=TARGET_CHAT_ID))
# async def handler(event):
#     """Listens for new messages and checks the sender's ID."""
#     sender = await event.get_sender()
#     message_text = event.message.message

#     print(f"📬 New message from User ID '{sender.id if sender else 'Unknown'}'")

#     # Controlla se l'ID del mittente corrisponde a quello autorizzato
#     if sender and sender.id == AUTHORIZED_USER_ID:
#         print("✅ Message is from the authorized user (YOU).")
#         required_keys = ["Trading Type:", "Time Frame:", "Signal Time:", "Direction:", "Trading Quantity:"]
#         if all(key in message_text for key in required_keys):
#             print("✅ Message is a valid signal. Starting process...")
#             screenshot_file_path = await execute_trade_flow()
#             send_report_email(message_text, screenshot_file_path)
#         else:
#             print("-> Message from you, but not a valid signal. Ignoring.")
#     else:
#         sender_id = sender.id if sender else "Unknown"
#         print(f"👤 Message ignored. Sender ID '{sender_id}' is not authorized.")

# async def main():
#     await client.start(PHONE_NUMBER)
#     print("🤖 Bot is running and connected to Telegram.")
#     print(f"👂 Listening for valid signals from User ID '{AUTHORIZED_USER_ID}' in chat ID '{TARGET_CHAT_ID}'...")
#     await client.run_until_disconnected()

# if __name__ == "__main__":
#     if not os.path.exists(AUTH_FILE):
#         print(f"CRITICAL: The authentication file '{AUTH_FILE}' does not exist.")
#         print("Please run 'save_auth.py' to create it before starting the bot.")
#     else:
#         asyncio.run(main())



import asyncio
import os
import re # Importato per il parsing del testo
from telethon import TelegramClient, events
from playwright.async_api import async_playwright
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# --- ⚙️ Configuration ---
# 1. Telegram Details (You must fill these in)
API_ID = 23609872  # Your API ID from my.telegram.org
API_HASH = '6d8206f84181146efb9f9a636d5321eb'
PHONE_NUMBER = '+393505183610'

# 2. Triggering Conditions (Updated for you)
TARGET_CHAT_ID = -1002359903313
# ⬇️ INSERISCI QUI IL TUO USER ID NUMERICO ⬇️
AUTHORIZED_USER_ID = 6765291471  # Sostituisci questo con il tuo ID

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

# --- 📧 Email Sending Function ---
def send_report_email(signal_text, screenshot_path=None):
    """Sends an email with the signal text and attaches a screenshot if available."""
    print(f"📧 Preparo l'email di report per {EMAIL_RECEIVER}...")
    try:
        msg = MIMEMultipart()
        msg['Subject'] = 'Nuovo Segnale di Trading Eseguito'
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg.attach(MIMEText(signal_text, 'plain'))
        if screenshot_path and os.path.exists(screenshot_path):
            with open(screenshot_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(screenshot_path))
                msg.attach(img)
            print("✅ Screenshot allegato all'email.")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("✅ Email di report inviata con successo!")
    except Exception as e:
        print(f"❌ Impossibile inviare l'email di report: {e}")

# --- 📝 Funzione per Estrarre i Dati dal Messaggio ---
def parse_signal(message_text):
    """Estrae i dati chiave dal testo del segnale usando espressioni regolari."""
    try:
        trading_type = re.search(r"Trading Type:\s*(.+)", message_text).group(1).strip().replace(' ', '')
        direction = re.search(r"Direction:\s*(.+)", message_text).group(1).strip()
        signal_time = re.search(r"Signal Time:\s*.*(\d{2}:\d{2})", message_text).group(1).strip()
        
        # Formatta il trading_type per corrispondere al sito (es. "ETH/USDT" -> "ETH / USDT")
        formatted_type = trading_type.replace('/', ' / ')

        return {
            "trading_type": formatted_type,
            "direction": direction,
            "signal_time": signal_time
        }
    except AttributeError:
        print("❌ Impossibile estrarre i dati dal messaggio. Formato non valido.")
        return None

# --- 🤖 Web Automation Function ---
async def execute_trade_flow(signal_data):
    """Esegue l'intero flusso di trading basato sui dati del segnale."""
    print("\n--- 🚀 Avvio Automazione Browser con Logica di Trading ---")
    screenshot_path = None
    if not os.path.exists(AUTH_FILE):
        print(f"❌ FATALE: File di autenticazione '{AUTH_FILE}' non trovato.")
        return None
        
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context(storage_state=AUTH_FILE, **p.devices['iPhone 13'])
        page = await context.new_page()
        try:
            # --- FASE 1: LOGIN E NAVIGAZIONE ---
            await page.goto(LOGIN_URL)
            await page.wait_for_timeout(2000)
            await page.locator(".login-btn").click()
            # await page.wait_for_url("https://txexss.com/h5/#/", timeout=10000)
            await page.wait_for_timeout(10000)
            await page.goto(TRADE_URL)
            await page.wait_for_timeout(2000)
            print("✅ Login e navigazione alla pagina di trade completati.")

            # --- FASE 2: CONTROLLO E SELEZIONE VALUTA ---
            currency_selector = 'span.fs-15.fw-700.ml-10'
            current_currency = await page.locator(currency_selector).inner_text()
            print(f"Valuta richiesta: '{signal_data['trading_type']}'. Valuta attuale: '{current_currency}'")

            if signal_data['trading_type'] not in current_currency:
                print("⚠️ Valuta non corretta. Apro il pannello di selezione...")
                await page.locator(currency_selector).click()
                await page.wait_for_timeout(2000)
                target_currency_in_panel = f"div.coin-item:has-text('{signal_data['trading_type']}')"
                await page.locator(target_currency_in_panel).click()
                await page.wait_for_timeout(2000)
                print(f"✅ Selezionata '{signal_data['trading_type']}' dal pannello.")
                
                await page.wait_for_function(f"document.querySelector('{currency_selector}').innerText.includes('{signal_data['trading_type']}')")
                print("✅ Verifica: la valuta è stata aggiornata correttamente.")

            # --- FASE 3: SELEZIONE DIREZIONE (CALL/PUT) ---
            print(f"Direzione richiesta: '{signal_data['direction']}'")
            if signal_data['direction'].upper() == 'CALL':
                direction_selector = ".btn.bg-success:has-text('CALL')"
                await page.locator(direction_selector).click()
            elif signal_data['direction'].upper() == 'PUT':
                direction_selector = ".btn.bg-danger:has-text('PUT')"
                await page.locator(direction_selector).click()
            else:
                raise ValueError(f"Direzione non valida: {signal_data['direction']}")
            
            print(f"✅ Cliccato su '{signal_data['direction']}'. In attesa del pannello di conferma.")
            await page.wait_for_timeout(2000)
            # --- FASE 4: GESTIONE PANNELLO CONFERMA ---
            target_minute = signal_data['signal_time'].split(':')[-1]
            current_selected_time = await page.locator('.van-picker-column__item--selected div').inner_text()
            current_hour = current_selected_time.split(':')[0]
            target_time_string = f"{current_hour}:{target_minute}"

            print(f"Imposto i minuti del trade a '{target_minute}' (ora completa: {target_time_string})")
            time_picker_item_selector = f'.van-picker-column__item div:has-text("{target_time_string}")'
            await page.locator(time_picker_item_selector).click()
            print("✅ Minuti impostati.")

            amount_selector = ".percentage-btn:has-text('1%')"
            print("Clicco su '1%' per la quantità.")
            await page.locator(amount_selector).click()
            print("✅ Quantità impostata.")

            # --- FASE 5: SCREENSHOT E CONFERMA FINALE ---
            print(f"📸 Eseguo lo screenshot prima della conferma finale...")
            await page.screenshot(path=SCREENSHOT_FILE)
            screenshot_path = SCREENSHOT_FILE

 # Determina il selettore corretto in base alla direzione del segnale
            if signal_data['direction'].upper() == 'CALL':
                final_confirm_selector = ".buy-btn.bg-success"
            else: # Se non è CALL, si presume sia PUT
                final_confirm_selector = ".buy-btn.bg-danger"

            print(f"Clicco sul pulsante di conferma finale '{signal_data['direction'].upper()}' con il selettore '{final_confirm_selector}'...")
            await page.locator(final_confirm_selector).click()
            print("✅ TRADE ESEGUITO!")

            await page.wait_for_timeout(190000)

        except Exception as e:
            print(f"❌ ERRORE durante il flusso di trading: {e}")
            if screenshot_path is None:
                 await page.screenshot(path=SCREENSHOT_FILE)
                 screenshot_path = SCREENSHOT_FILE
        finally:
            await browser.close()
            print("--- ✅ Flusso di Automazione Terminato ---\n")
            return screenshot_path

# --- 📞 Telegram Client & Handler ---
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHAT_ID))
async def handler(event):
    """Ascolta i messaggi, controlla il mittente, estrae i dati ed esegue il trade."""
    sender = await event.get_sender()
    message_text = event.message.message

    print(f"📬 Nuovo messaggio da: {sender.username} User ID '{sender.id if sender else 'Sconosciuto'}'")

    if sender and sender.id == AUTHORIZED_USER_ID:
        print(f"✅ Messaggio dall'utente autorizzato: {sender.username}")
        required_keys = ["Trading Type:", "Direction:", "Signal Time:"]
        
        if all(key in message_text for key in required_keys):
            print("✅ Formato del messaggio valido. Estraggo i dati...")
            signal_data = parse_signal(message_text)
            
            if signal_data:
                print(f"Dati estratti: {signal_data}")
                screenshot_file_path = await execute_trade_flow(signal_data)
                send_report_email(message_text, screenshot_file_path)
        else:
            print(f"-> ❌ Messaggio da: {sender.username}, ma non è un segnale valido. Ignoro.")
    else:
        sender_id = sender.id if sender else "Sconosciuto"
        print(f"✖️    Messaggio ignorato. Mittente: {sender.username}, ID '{sender_id}' non autorizzato.")

async def main():
    """Connette il client e lo fa funzionare per sempre."""
    await client.start(PHONE_NUMBER)
    print("🤖 Bot avviato e connesso a Telegram.")
    print(f"👂 In ascolto per segnali validi da User ID '{AUTHORIZED_USER_ID}' nella chat '{TARGET_CHAT_ID}'...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    if not os.path.exists(AUTH_FILE):
        print(f"CRITICO: Il file di autenticazione '{AUTH_FILE}' non esiste.")
        print("Esegui prima 'save_auth.py' per crearlo.")
    else:
        asyncio.run(main())