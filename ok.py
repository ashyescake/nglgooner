import requests, time, random, os, threading
from colorama import init, Fore, Style
from queue import Queue

init(autoreset=True)

def fetch_proxies():
    print(Fore.CYAN + "🔄 Mengambil proxy fresh...")
    urls = [
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/http/data.txt",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/https/data.txt"
    ]
    
    all_proxies = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                proxies = [line.strip() for line in r.text.splitlines() if line.strip()]
                all_proxies.extend(proxies)
        except:
            pass
    
    unique = list(dict.fromkeys(all_proxies))
    print(Fore.GREEN + f"✅ Total proxy diambil: {len(unique)}\n")
    return unique

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.CYAN + "NGL AUTO PROXY SPAMMER")
    print(Fore.YELLOW + "Hanya valid proxy yang dihitung\n")

def spam_worker(username, message, queue, success_count, proxies):
    while not queue.empty():
        i = queue.get()
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}

        headers = {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36"
        ])}

        payload = {
            "username": username,
            "question": message,
            "deviceId": f"web-{random.randint(100000000,999999999)}"
        }

        try:
            r = requests.post("https://ngl.link/api/submit", 
                            json=payload, 
                            headers=headers, 
                            proxies=proxy_dict, 
                            timeout=10)
            
            if r.status_code == 200:
                success_count[0] += 1
                print(f"{Fore.GREEN}[✓] {i:3d} | SUCCESS | Valid Proxy")
            else:
                print(f"{Fore.RED}[✗] {i:3d} | Failed")
        except:
            print(f"{Fore.YELLOW}[!] {i:3d} | Proxy Invalid")

        queue.task_done()
        time.sleep(random.uniform(0.6, 1.5))

# ================== MAIN ==================
banner()
proxies = fetch_proxies()

username = input(Fore.WHITE + "Target Username: " + Fore.YELLOW)
message = input(Fore.WHITE + "Pesan: " + Fore.YELLOW)
amount = int(input(Fore.WHITE + "Jumlah Spam: " + Fore.YELLOW))
threads = int(input(Fore.WHITE + "Thread (10-30): " + Fore.YELLOW) or "20")

print(Fore.MAGENTA + f"\n🚀 Mulai spam... Hanya yang berhasil akan dihitung!\n")

queue = Queue()
success = [0]

for i in range(1, amount + 1):
    queue.put(i)

for _ in range(threads):
    t = threading.Thread(target=spam_worker, args=(username, message, queue, success, proxies))
    t.daemon = True
    t.start()

queue.join()

print(Fore.CYAN + f"\n{'='*55}")
print(Fore.GREEN + f"SELESAI! Berhasil Dikirim: {success[0]}/{amount}")
print(Fore.CYAN + f"{'='*55}")
