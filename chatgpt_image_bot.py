import random
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ══════════════════════════════════════════════════════
#  CONFIGURATION — Edit these before running
# ══════════════════════════════════════════════════════

IMAGES_FOLDER    = r"C:\Users\am00610\Downloads\WhatsApp Unknown 2026-04-30 at 8.18.42 PM"  # folder with your images
DONE_FOLDER      = r"C:\Users\am00610\Downloads\WhatsApp Unknown 2026-04-30 at 8.18.42 PM\used"  # used images go here
EDGE_DRIVER_PATH = r"C:\Users\am00610\Downloads\edgedriver_win64\msedgedriver.exe"            # path to your EdgeDriver .exe
EDGE_PROFILE_DIR = r"C:\Users\am00610\AppData\Local\Microsoft\Edge\User Data"  # your Edge profile

PROMPT_TEXT  = (
    "Generate an image: wide banner panoramic composition of this product, "
    "clean and aesthetically arranged, professional product photography, "
    "soft diffused studio lighting, subtle natural shadows, high detail, "
    "sharp focus, realistic textures, balanced exposure, clean minimal background, "
    "premium commercial look, centered composition, isolated subject, "
    "no clutter, no text, no watermark. Wide 4:1 aspect ratio."
)
WAIT_MINUTES = 5                   # minutes to wait between images

# Supported image file types
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp')

# ══════════════════════════════════════════════════════

def get_image_list(folder):
    """Collect all image files from the folder (not subfolders)."""
    images = [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(IMAGE_EXTENSIONS)
        and os.path.isfile(os.path.join(folder, f))
    ]
    return images

def move_to_done(image_path, done_folder):
    """Move a processed image to the done folder."""
    os.makedirs(done_folder, exist_ok=True)
    filename = os.path.basename(image_path)
    destination = os.path.join(done_folder, filename)

    # If a file with the same name already exists in done, rename it
    if os.path.exists(destination):
        name, ext = os.path.splitext(filename)
        destination = os.path.join(done_folder, f"{name}_{int(time.time())}{ext}")

    shutil.move(image_path, destination)
    print(f"  ✅  Moved '{filename}' → done folder.")


def setup_driver():
    """Launch Microsoft Edge using your existing logged-in profile."""
    options = Options()
    options.add_argument("--start-maximized")
    # Reuse your existing Edge profile so ChatGPT login is already active
    #options.add_argument(f"--user-data-dir={EDGE_PROFILE_DIR}")
    options.add_argument(r"--user-data-dir=C:\EdgeAutomationProfile")
    #options.add_argument("--profile-directory=Default")

    # Suppress automation banners (cosmetic)
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_experimental_option("useAutomationExtension", False)

    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def find_element_any(driver, selectors, timeout=20):
    """Try a list of CSS selectors one by one and return the first match."""
    for selector in selectors:
        try:
            el = WebDriverWait(driver, timeout / len(selectors)).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return el
        except Exception:
            continue
    raise Exception(f"None of the selectors matched: {selectors}")

def send_image_to_chatgpt(driver, image_path, prompt):
    """Navigate to ChatGPT, upload the image, type the prompt, and submit."""
    wait = WebDriverWait(driver, 40)

    print(f"  🌐  Opening ChatGPT...")
    driver.get("https://chatgpt.com/")
    time.sleep(random.uniform(5, 9))  # let the page fully load

    # ── Step 1: Inject file directly into hidden file input ──
    # More robust than clicking the attach button since ChatGPT UI changes often
    print(f"  🖼️   Uploading image: {os.path.basename(image_path)}")
    try:
        # Make all file inputs visible so Selenium can interact with them
        driver.execute_script("""
            document.querySelectorAll('input[type=file]').forEach(el => {
                el.style.display = 'block';
                el.style.visibility = 'visible';
                el.style.opacity = '1';
                el.style.position = 'fixed';
                el.style.top = '0';
                el.style.left = '0';
                el.style.zIndex = '9999';
            });
        """)
        time.sleep(1)
        file_input = find_element_any(driver, [
            "input[type='file']",
            "input[accept*='image']",
            "input[multiple][type='file']",
        ])
        file_input.send_keys(image_path)
        print(f"  ✅  Image attached via file input.")
        time.sleep(random.uniform(3, 6))

    except Exception:
        # Fallback: try clicking the attach button first, then find file input
        print(f"  📎  Trying attachment button fallback...")
        attach_selectors = [
            "button[aria-label='Attach files']",
            "button[aria-label='Add attachments']",
            "button[aria-label='Upload']",
            "button[data-testid='attach-button']",
            "label[for*='file']",
            "button[class*='attach']",
            "button[class*='upload']",
        ]
        for selector in attach_selectors:
            try:
                btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                btn.click()
                print(f"  ✅  Clicked attach button: {selector}")
                time.sleep(2)
                break
            except Exception:
                continue

        driver.execute_script("""
            document.querySelectorAll('input[type=file]').forEach(el => {
                el.style.display = 'block';
                el.style.visibility = 'visible';
                el.style.opacity = '1';
            });
        """)
        time.sleep(1)
        file_input = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='file']")
        ))
        file_input.send_keys(image_path)
        time.sleep(4)

    # ── Step 2: Type the prompt ──
    print(f"  ✍️   Typing prompt...")
    textarea = find_element_any(driver, [
        "#prompt-textarea",
        "div[contenteditable='true']",
        "textarea[placeholder]",
        "div[role='textbox']",
    ], timeout=20)
    textarea.click()
    textarea.send_keys(prompt)
    time.sleep(1)

    # ── Step 3: Click Send ──
    print(f"  📤  Sending message...")
    send_btn = find_element_any(driver, [
        "button[data-testid='send-button']",
        "button[aria-label='Send message']",
        "button[aria-label='Send prompt']",
        "button[class*='send']",
    ], timeout=20)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='send-button']")))
    send_btn.click()
    print(f"  ✅  Message sent successfully.")


def countdown(minutes):
    """Show a live countdown in the terminal."""
    total_seconds = minutes * 60
    for remaining in range(total_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        print(f"\r  ⏳  Next image in: {mins:02d}:{secs:02d}", end="", flush=True)
        time.sleep(1)
    print()  # newline after countdown


def main():
    os.makedirs(DONE_FOLDER, exist_ok=True)

    images = get_image_list(IMAGES_FOLDER)

    if not images:
        print("❌  No images found in the folder. Check your IMAGES_FOLDER path.")
        return

    print(f"╔══════════════════════════════════════╗")
    print(f"   ChatGPT Image Bot — {len(images)} image(s) found")
    print(f"╚══════════════════════════════════════╝\n")

    driver = setup_driver()

    try:
        for i, image_path in enumerate(images):
            filename = os.path.basename(image_path)
            print(f"\n[{i+1}/{len(images)}] ── {filename}")

            send_image_to_chatgpt(driver, image_path, PROMPT_TEXT)
            move_to_done(image_path, DONE_FOLDER)

            # Wait between images (skip wait after the last one)
            if i < len(images) - 1:
                print(f"\n  Waiting {WAIT_MINUTES} minutes before next image...")
                countdown(WAIT_MINUTES)

        print(f"\n🎉  All {len(images)} image(s) processed successfully!")

    except Exception as e:
        print(f"\n❌  An error occurred: {e}")
        print("     Tip: ChatGPT's UI may have changed. Check the CSS selectors.")

    finally:
        input("\nPress ENTER to close the browser...")
        driver.quit()

if __name__ == "__main__":
    main()
