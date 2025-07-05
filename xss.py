import requests
import subprocess
import urllib.parse
import random
import time
import base64
from datetime import datetime
import os

BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 9; Mobile; rv:91.0)",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)"
]

def load_payloads(filename):
    if not os.path.exists(filename):
        print(f"{RED}[!] File payload '{filename}' tidak ditemukan.{RESET}")
        exit()
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def encode_payloads(payload):
    return list(set([
        payload,
        urllib.parse.quote(payload),
        urllib.parse.quote(urllib.parse.quote(payload)),
        base64.b64encode(payload.encode()).decode(),
        ''.join(['\\x{:02x}'.format(ord(c)) for c in payload]),
        ''.join(['\\u{:04x}'.format(ord(c)) for c in payload])
    ]))

def random_headers(param=None, payload=None):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Referer": f"https://{random.choice(['google.com', 'bing.com', 'duckduckgo.com'])}/",
        "X-Forwarded-For": f"{random.randint(10,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        "X-Real-IP": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
        "X-Originating-IP": "127.0.0.1",
        "X-Custom-IP-Authorization": "127.0.0.1",
        "X-Original-URL": "/",
        "Connection": "close",
        "Cookie": f"PHPSESSID={random.randint(100000,999999)}"
    }
    if param and payload:
        headers[param] = payload
    return headers

def run_curl(url, timeout):
    cmd = f"curl -o /dev/null -s -w 'Code: %{{http_code}} | Total Time: %{{time_total}}s\\n' --max-time {timeout} '{url}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"{BLUE}Curl Result untuk {url}:{RESET}")
    print(result.stdout)

def extract_param_name(url):
    parsed = urllib.parse.urlparse(url)
    if "=" in url and "?" in url:
        return url.split("?")[1].split("=")[0]
    return "q"

def check_xss(base_url, timeout, payload_list):
    param_name = extract_param_name(base_url)
    print(f"{YELLOW}[i] Parameter yang digunakan: {param_name}{RESET}")

    for payload in payload_list:
        encoded_versions = encode_payloads(payload)

        for encoded in encoded_versions:
            try:
                headers = random_headers(param_name, encoded)
                full_get_url = f"{base_url}{encoded}"

                response = requests.get(full_get_url, headers=headers, timeout=timeout, allow_redirects=False)

                if response.status_code == 403:
                    print(f"{RED}[-] waduh kacaw nih, kena 403 Detected! Switch ke POST...{RESET}")
                    post_data = {param_name: encoded}
                    response = requests.post(base_url.split("?")[0], data=post_data, headers=headers, timeout=timeout)

                if response.status_code == 403:
                    print(f"{RED}[-] Masih kena 403 bjirr, waitt Coba header injection...{RESET}")
                    headers = random_headers()
                    headers[param_name] = encoded
                    response = requests.get(base_url.split("?")[0], headers=headers, timeout=timeout)

                if "alert" in response.text.lower() or encoded.lower() in response.text.lower():
                    now = datetime.now().strftime("%H:%M:%S")
                    print(f"{GREEN}[{now}] ✅ XSS Terdeteksi!{RESET}")
                    print(f"{GREEN}Payload: {encoded}{RESET}")
                    print(f"{GREEN}URL: {response.url}{RESET}")
                    print("-" * 50)
                else:
                    print(f"{RED}[-] Tidak reflektif: {encoded}{RESET}")

                time.sleep(random.uniform(1.5, 3.0))

            except Exception as e:
                print(f"{RED}[!] Error: {e}{RESET}")

print(f"{BLUE}===== RenXploit XSS Advanced Scanner ====={RESET}")
website_url = input("Masukkan URL target (kosong param): ").strip()
payload_file = input("Masukkan nama file payload (ex: payloads.txt): ").strip()

run_curl(website_url, timeout=5)

try:
    timeout = int(input("Masukkan timeout (default: 5): "))
except:
    timeout = 5

payloads = load_payloads(payload_file)
print(f"{BLUE}[*] Mulai scanning terhadap: {website_url} dengan {len(payloads)} payload...{RESET}")
check_xss(website_url, timeout, payloads)
