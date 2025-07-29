import asyncio
import os
from playwright.async_api import async_playwright

# --- Configuration ---
AUTH_FILE = 'auth.json'
LOGIN_URL = 'https://txexss.com/h5/#/login'
TRADE_URL = 'https://txexss.com/h5/#/trade'

async def test_trade_flow():
    """
    Tests the full flow: login -> navigate to trade -> click CALL.
    """
    print("🚀 Starting trade flow test...")

    if not os.path.exists(AUTH_FILE):
        print(f"\n❌ Error: Authentication file '{AUTH_FILE}' not found.")
        print("Please run 'save_auth.py' first to create it.")
        return

    async with async_playwright() as p:
        # Launch the browser visibly
        browser = await p.chromium.launch(headless=False, slow_mo=500) # slow_mo adds a delay to see actions
        
        # Load the saved session from auth.json
        context = await browser.new_context(
            storage_state=AUTH_FILE,
            **p.devices['iPhone 13']
        )
        page = await context.new_page()

        try:
            # 1. Navigate to the login page
            print(f"Navigating to login page: {LOGIN_URL}")
            await page.goto(LOGIN_URL)

            # 2. As requested, click the main "Login" button
            # NOTE: With auth.json loaded, this step might be redundant if the site
            # auto-redirects, but we are including it as requested.
            login_button_selector = ".login-btn"
            print(f"Clicking login button: '{login_button_selector}'")
            await page.locator(login_button_selector).click()
            
            # Wait for the URL to change, indicating a successful login/redirect
            await page.wait_for_url("https://txexss.com/h5/#/home", timeout=10000)
            print("✅ Login/redirect successful.")

            # 3. Navigate to the trade page
            print(f"Navigating to trade page: {TRADE_URL}")
            await page.goto(TRADE_URL)
            
            # 4. Find and click the "CALL" button
            # This selector specifically targets the green "CALL" button.
            call_button_selector = ".btn.bg-success:has-text('CALL')"
            print(f"Looking for CALL button with selector: '{call_button_selector}'")
            call_button = page.locator(call_button_selector)
            
            await call_button.wait_for(state='visible', timeout=10000)
            print("✅ CALL button found. Clicking it now.")
            await call_button.click()
            print("✅ Clicked the CALL button.")

            # Pause for a few seconds to observe the result
            await page.wait_for_timeout(3000)

        except Exception as e:
            print(f"\n❌ An error occurred during the flow.")
            print(f"Error details: {e}")
        
        finally:
            # 5. Take a final screenshot and close
            screenshot_path = "call_button_click_result.png"
            print(f"📸 Taking final screenshot...")
            await page.screenshot(path=screenshot_path)
            await browser.close()
            print(f"🛑 Browser closed. Screenshot saved to '{screenshot_path}'.")

if __name__ == "__main__":
    asyncio.run(test_trade_flow())