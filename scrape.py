from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os

CHROMEDRIVER_PATH = "./chromedriver.exe"

def scrape_website(website):
    print("Setting up the browser...")
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    service = Service(CHROMEDRIVER_PATH)

    with webdriver.Chrome(service=service, options=options) as driver:
        print("Opening the website...")
        driver.get(website)

        # Prompt user to solve CAPTCHA
        input("Solve the CAPTCHA manually and press Enter to continue...")

        # Wait for a specific element or condition (e.g., main content or body tag)
        print("Waiting for the page to fully load...")
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as e:
            print(f"Error: Page did not load in time: {e}")
            return None

        print("Scraping page content...")
        html = driver.page_source
        print("Page content successfully scraped!")
        return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


# Example Usage
if __name__ == "__main__":
    url = input("Enter the website URL: ")
    raw_html = scrape_website(url)

    if raw_html:
        body_content = extract_body_content(raw_html)
        cleaned_content = clean_body_content(body_content)
        print("\n=== Cleaned Content ===\n")
        print(cleaned_content[:1000])  # Show the first 1000 characters as a preview
