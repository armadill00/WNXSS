<h1>🛡️ Advanced XSS Scanner</h1>

A powerful Python-based XSS vulnerability scanner that tests web applications for Reflected XSS, DOM-Based XSS, and WAF bypass techniques.

<h2>⚡ Features</h2>

🚀 Automated Form Scanning - Detects and tests input fields for XSS.

🎭 Bypasses WAF Protections - Uses URL encoding, hex encoding, and polyglot payloads.

🔍 DOM-Based XSS Detection - Uses Selenium WebDriver for JavaScript-based attacks.

🔄 Stored XSS Testing - Manually re-checks stored payloads.

🛠 Header-Based XSS Testing - Checks if input is reflected in HTTP headers.

<h2>📌 Installation</h2>

1️⃣ Install Dependencies

Ensure you have Python 3+ installed.

pip install requests beautifulsoup4 selenium

2️⃣ Download ChromeDriver

Find your Chrome version: Go to chrome://settings/help in Chrome.

Download matching chromedriver from: ChromeDriver Download

Move chromedriver to a known location (e.g., /usr/local/bin/ or C:\chromedriver.exe)

<h2>🚀 Usage</h2>

Run the script and provide a target URL:

python xss_scanner.py

Enter the website URL when prompted:

Enter the target URL to scan: https://example.com

<h2>🛡️ Supported XSS Techniques</h2>

✅ Reflected XSS (Injects payload into form fields)
✅ DOM-Based XSS (Uses Selenium to detect JavaScript-executed XSS)
✅ Stored XSS (Checks if input remains stored in page source)
✅ WAF Bypass Techniques (Encodes payloads in Hex, URL, and Polyglot)
✅ Header Injection XSS (Tests reflection in HTTP headers)

⚠️ Disclaimer

This tool is for educational and security testing purposes only. Do not use it on websites without permission. Unauthorized testing may violate laws and regulations.

