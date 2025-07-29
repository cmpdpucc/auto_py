import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) # Must be non-headless to log in
        context = await browser.new_context()
        page = await context.new_page()

        # Go to the login page and wait for you to log in manually
        await page.goto("https://txexss.com/h5/#/login")
        print("\n" + "="*50)
        print("Please log in to the website manually in the browser window.")
        print("Once you are logged in, close the browser window.")
        print("="*50 + "\n")

        # This will pause the script until the page is closed
        await page.wait_for_event('close')

        # Save the storage state to a file
        await context.storage_state(path="auth.json")
        print("✅ Authentication state saved to auth.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())