from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    file_path = "C:\\GDG AGENTATHON\\indigo_simple.html"
    page.goto(f"file://{file_path}")
    print("✅ Page loaded")
    
    # Fill fields
    page.locator('[name="pnr-booking-ref"]').fill("TEST99")
    print("✅ Filled PNR")
    
    page.locator('[name="email-last-name"]').fill("Doe")
    print("✅ Filled Email")
    
    time.sleep(1)
    
    # Click submit with JS
    print("🔄 Clicking submit...")
    page.evaluate("document.getElementById('submitBtn').click()")
    print("✅ Clicked!")
    
    time.sleep(5)
    page.screenshot(path="test_screenshot.png")
    print("✅ Screenshot saved")
    
    browser.close()
