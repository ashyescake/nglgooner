import requests, time, random, os, threading
from colorama import init, Fore, Style
from queue import Queue

init(autoreset=True)

# ================== AUTO AMBIL PROXY ==================
def fetch_proxies():
    print(Fore.CYAN + "🔄 Mengambil proxy fresh dari Proxifly...")
    urls = [
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/https/data.txt",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt"
    ]
    
    all_proxies = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                proxies = [line.strip() for line in r.text.splitlines() if line.strip() and "://" in line]
                all_proxies.extend(proxies)
                print(Fore.GREEN + f"✅ Berhasil ambil {len(proxies)} proxy")
        except:
            print(Fore.YELLOW + "⚠️ Gagal ambil satu sumber proxy")
    
    unique = list(dict.fromkeys(all_proxies))
    print(Fore.GREEN + f"Total proxy siap: {len(unique)}\n")
    return unique

# ================== BANNER ==================
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.CYAN + """
    ███╗   ██╗ ██████╗ ██╗     ███████╗██████╗  █████╗  ██████╗███████╗
    ████╗  ██║██╔═══██╗██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██╔██╗ ██║██║   ██║██║     █████╗  ██████╔╝███████║██║     █████╗  
    """)
    print(Fore.YELLOW + "          NGL AUTO PROXY SPAMMER\n")

# ================== WORKER ==================
def spam_worker(username, message, queue, success_count, proxies):
    while not queue.empty():
        i = queue.get()
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}

        headers = {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
        ])}

        payload = {
            "username": username,
            "question": message,
            "deviceId": f"web-{random.randint(100000000,999999999)}",
            "gameSlug": "", "referrer": ""
        }

        try:
            r = requests.post("https://ngl.link/api/submit", 
                            json=payload, headers=headers, 
                            proxies=proxy_dict, timeout=12)
            
            if r.status_code == 200:
                success_count[0] += 1
                print(f"{Fore.GREEN}[✓] {i} Success")
            else:
                print(f"{Fore.RED}[✗] {i} Failed")
        except:
            print(f"{Fore.YELLOW}[!] {i} Proxy mati")

        queue.task_done()
        time.sleep(random.uniform(0.5, 1.3))

# ================== MAIN ==================
banner()
proxies = fetch_proxies()

if len(proxies) < 10:
    print(Fore.RED + "Proxy terlalu sedikit, coba lagi nanti.")
    exit()

username = input(Fore.WHITE + "Target Username: " + Fore.YELLOW)
message = input(Fore.WHITE + "Pesan: " + Fore.YELLOW)
amount = int(input(Fore.WHITE + "Jumlah Spam: " + Fore.YELLOW))
threads = int(input(Fore.WHITE + "Thread (10-40): " + Fore.YELLOW) or "20")

print(Fore.MAGENTA + f"\n🚀 Mulai spam dengan {threads} threads...\n")

queue = Queue()
success = [0]

for i in range(1, amount + 1):
    queue.put(i)

for _ in range(threads):
    t = threading.Thread(target=spam_worker, args=(username, message, queue, success, proxies))
    t.daemon = True
    t.start()

queue.join()

print(Fore.CYAN + f"\n{'='*60}")
print(Fore.GREEN + f"SELESAI! Berhasil: {success[0]}/{amount}")
print(Fore.CYAN + f"{'='*60}")
