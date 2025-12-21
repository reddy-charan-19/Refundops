from playwright.sync_api import sync_playwright
import time
import os

# --- 1. INDIGO PROCESS ---
def start_indigo_process(pnr_number):
    print(f"🤖 INDIGO BOT: Opening local portal for PNR {pnr_number}...", flush=True)
    run_local_bot("indigo_simple.html", pnr_number, "Indigo")

# --- 2. AIR INDIA PROCESS ---
def start_airindia_process(pnr_number):
    print(f"🤖 AIR INDIA BOT: Opening local portal for PNR {pnr_number}...", flush=True)
    run_local_bot("airindia.html", pnr_number, "Air India")

# --- SHARED LOGIC (The "Smart" Function) ---
def run_local_bot(filename, pnr, airline_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headless=False so you see it
        page = browser.new_page()
        
        # 1. Load the Local File
        file_path = os.path.abspath(filename)
        if not os.path.exists(file_path):
            print(f"❌ ERROR: Could not find '{filename}' in the folder.")
            print(f"👉 Please rename your downloaded HTML file to '{filename}'")
            browser.close()
            return

        page.goto(f"file://{file_path}")
        print(f"📂 Loaded {airline_name} portal.", flush=True)

        try:
            # 2. Fill form fields
            print("✍️ Filling Form Details...", flush=True)
            
            # Wait for page to be ready
            time.sleep(2)

            # Fill PNR
            try:
                page.locator('[name="pnr-booking-ref"]').wait_for(state="visible", timeout=5000)
                page.locator('[name="pnr-booking-ref"]').fill(pnr)
                print(f"✅ Filled PNR: {pnr}", flush=True)
            except Exception as e1:
                try:
                    page.locator("#pnr").wait_for(state="visible", timeout=5000)
                    page.locator("#pnr").fill(pnr)
                    print(f"✅ Filled PNR: {pnr}", flush=True)
                except Exception as e2:
                    print(f"❌ Could not find PNR field: {e2}", flush=True)

            # Fill Email/Last Name
            try:
                page.locator('[name="email-last-name"]').wait_for(state="visible", timeout=5000)
                page.locator('[name="email-last-name"]').fill("Atmuri Shanmukha Praneet")
                print("✅ Filled Email/Last Name", flush=True)
            except Exception as e1:
                try:
                    page.locator("#email").wait_for(state="visible", timeout=5000)
                    page.locator("#email").fill("Praneetatmuri@gmail.com")
                    print("✅ Filled Email", flush=True)
                except Exception as e2:
                    print(f"⚠️ Could not find Email field: {e2}", flush=True)

            # 3. Click Submit
            print("🖱️ Clicking Submit...", flush=True)
            time.sleep(1)
            
            try:
                page.evaluate("document.getElementById('submitBtn').click()")
                print("✅ Clicked submit button!", flush=True)
                time.sleep(5)
            except Exception as e:
                print(f"❌ Click failed: {e}", flush=True)

            # 4. SUCCESS SCREENSHOT
            time.sleep(2)
            screenshot_name = f"{airline_name.lower()}_success.png"
            page.screenshot(path=screenshot_name)
            print(f"✅ Success! Screenshot saved: {screenshot_name}")

        except Exception as e:
            print(f"❌ Error on {airline_name} page: {e}")
        
        browser.close()
        