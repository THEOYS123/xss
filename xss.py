import requests
import urllib.parse
import base64
import os
import time
import random
from datetime import datetime
RED='\x1b[91m'
GREEN='\x1b[92m'
YELLOW='\x1b[93m'
BLUE='\x1b[94m'
RESET='\x1b[0m'
hasil_scan=[]
def load_user_agents(filename='user.txt'):
	if not os.path.exists(filename):print(f"{YELLOW}[!] File 'useragents.txt' tidak ditemukan, pakai default user-agent.{RESET}");return['Mozilla/5.0 (Windows NT 10.0; Win64; x64)','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)','Mozilla/5.0 (X11; Linux x86_64)','Mozilla/5.0 (Linux; Android 9; Mobile; rv:91.0)','Googlebot/2.1 (+http://www.google.com/bot.html)']
	with open(filename,'r')as f:return[ua.strip()for ua in f if ua.strip()]
def random_headers(user_agents):return{'User-Agent':random.choice(user_agents),'X-Forwarded-For':f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",'X-Real-IP':'127.0.0.1','Referer':'https://google.com','Cookie':f"SESSIONID={random.randint(100000,999999)}",'Connection':'keep-alive'}
def load_payloads(file_name):
	if not os.path.exists(file_name):print(f"{RED}[!] File payload '{file_name}' tidak ditemukan!{RESET}");exit()
	with open(file_name,'r')as f:return[line.strip()for line in f if line.strip()]
def encode_variants(payload):return list(set([payload,urllib.parse.quote(payload),urllib.parse.quote_plus(payload),urllib.parse.quote(urllib.parse.quote(payload)),base64.b64encode(payload.encode()).decode(),''.join(['\\x{:02x}'.format(ord(c))for c in payload])]))
def extract_param_name(url):parsed=urllib.parse.urlparse(url);qs=urllib.parse.parse_qs(parsed.query);return list(qs.keys())[0]if qs else'q'
def simpan_hasil(hasil_file):
	if hasil_scan:
		with open(hasil_file,'w')as f:
			for hasil in hasil_scan:f.write(hasil+'\n')
		print(f"{GREEN}[✔] Hasil disimpan ke: {hasil_file}{RESET}")
	else:print(f"{YELLOW}[!] Tidak ada hasil XSS untuk disimpan.{RESET}")
def check_xss(base_url,timeout,payload_list,user_agents,use_encrypt,hasil_file):
	param_name=extract_param_name(base_url);print(f"{YELLOW}[i] Parameter digunakan: {param_name}{RESET}")
	try:
		for payload in payload_list:
			variants=encode_variants(payload)if use_encrypt else[payload]
			for p in variants:
				try:
					headers=random_headers(user_agents);full_url=f"{base_url}{p}";response=requests.get(full_url,headers=headers,timeout=timeout,allow_redirects=False)
					if payload in response.text and'&lt;'not in response.text and'&gt;'not in response.text and'<'in payload and'>'in payload:now=datetime.now().strftime('%H:%M:%S');print(f"\n{GREEN}[{now}] ✅ XSS Terdeteksi!{RESET}");print(f"{GREEN}Payload: {payload}{RESET}");print(f"{GREEN}URL: {full_url}{RESET}");print('-'*50);hasil_scan.append(f"[{now}] XSS => {full_url} | Payload: {payload}")
					else:print(f"{RED}[-] Tidak reflektif: {p}{RESET}")
					time.sleep(random.uniform(.4,1.2))
				except Exception as e:print(f"{RED}[!] Error saat request: {e}{RESET}")
	except KeyboardInterrupt:print(f"\n{YELLOW}[!] Dihentikan paksa (Ctrl+C)! Menyimpan hasil...{RESET}");simpan_hasil(hasil_file);exit()
	simpan_hasil(hasil_file)
print(f"{BLUE}===== RenXploit XSS Reflected Scanner v3 FINAL ====={RESET}")
url=input('Masukkan URL target (kosong param, contoh: https://target.com/page.php?id=): ').strip()
if not url.startswith('http://')and not url.startswith('https://'):print(f"{RED}[!] URL harus diawali http:// atau https://{RESET}");exit()
payload_file=input('Masukkan nama file payload (contoh: payload.txt): ').strip()
hasil_file=input('Masukkan nama file untuk menyimpan hasil (contoh: hasil.txt): ').strip()
encrypt_input=input('Gunakan encoded/encrypt payload? (y/n): ').strip().lower()
use_encrypt=encrypt_input=='y'
try:timeout=int(input('Masukkan timeout (default 5): ').strip()or 5)
except:timeout=5
payloads=load_payloads(payload_file)
user_agents=load_user_agents()
print(f"{BLUE}[*] Mulai scanning terhadap: {url} dengan {len(payloads)} payload...{RESET}")
check_xss(url,timeout,payloads,user_agents,use_encrypt,hasil_file)
