import requests, time, random, os, threading
from colorama import init, Fore, Style
from queue import Queue

init(autoreset=True)

# ================== LOAD PROXIES ==================
def load_proxies(file="proxies.txt"):
    try:
        with open(file, "r") as f:
            proxies = [line.strip() for line in f if line.strip() and "://" in line]
            print(Fore.GREEN + f"✅ Loaded {len(proxies)} proxies")
            return proxies
    except:
        print(Fore.RED + "❌ proxies.txt tidak ditemukan!")
        return []

proxies = load_proxies()

# ================== BANNER ==================
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.CYAN + """
    ███╗   ██╗ ██████╗ ██╗     ███████╗██████╗  █████╗  ██████╗███████╗
    ████╗  ██║██╔═══██╗██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██╔██╗ ██║██║   ██║██║     █████╗  ██████╔╝███████║██║     █████╗  
    """)
    print(Fore.YELLOW + "          NGL SPAMMER MULTI-THREAD + PROXY\n")

# ================== WORKER ==================
def spam_worker(username, message, queue, success_count):
    while not queue.empty():
        i = queue.get()
        if not proxies:
            break
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}

        headers = {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"
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
            print(f"{Fore.YELLOW}[!] {i} Proxy Error")

        queue.task_done()
        time.sleep(random.uniform(0.3, 0.8))

# ================== MAIN ==================
banner()
username = input(Fore.WHITE + "Target Username: " + Fore.YELLOW)
message = input(Fore.WHITE + "Pesan: " + Fore.YELLOW)
amount = int(input(Fore.WHITE + "Jumlah Spam: " + Fore.YELLOW))
threads = int(input(Fore.WHITE + "Jumlah Thread (disarankan 10-30): " + Fore.YELLOW) or 15)

print(Fore.MAGENTA + f"\n🚀 Mulai spam dengan {threads} threads...\n")

queue = Queue()
success = [0]

for i in range(1, amount + 1):
    queue.put(i)

# Start threads
for _ in range(threads):
    t = threading.Thread(target=spam_worker, args=(username, message, queue, success))
    t.daemon = True
    t.start()

queue.join()

print(Fore.CYAN + f"\n{'='*60}")
print(Fore.GREEN + f"SELESAI! Berhasil: {success[0]}/{amount}")
print(Fore.CYAN + f"{'='*60}")
