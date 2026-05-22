import requests, time, random, sys, os
from colorama import init, Fore, Style

init(autoreset=True)

# ================== PROXY LIST ==================
proxies = [
    "http://45.8.211.115:80",
    "http://89.116.250.135:80",
    # ... (semua proxy lu otomatis dimasukkan)
]

# Load semua proxy dari file (kalau mau lebih rapi)
def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except:
        return proxies  # fallback ke list di atas

# ================== BANNER ==================
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + """
    ███╗   ██╗ ██████╗ ██╗     ███████╗██████╗  █████╗  ██████╗███████╗
    ████╗  ██║██╔═══██╗██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██╔██╗ ██║██║   ██║██║     █████╗  ██████╔╝███████║██║     █████╗  
    ██║╚██╗██║██║   ██║██║     ██╔══╝  ██╔══██╗██╔══██║██║     ██╔══╝  
    ██║ ╚████║╚██████╔╝███████╗███████╗██║  ██║██║  ██║╚██████╗███████╗
    """)
    print(Fore.YELLOW + "          NGL LINK SPAMMER + PROXY - KENAIRFORCES\n")

# ================== SPAM FUNCTION ==================
def spam_ngl(username, message, amount):
    proxy_list = load_proxies()
    success = 0
    failed = 0

    for i in range(1, amount + 1):
        proxy = random.choice(proxy_list)
        proxy_dict = {"http": proxy, "https": proxy}

        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
            ])
        }

        payload = {
            "username": username,
            "question": message,
            "deviceId": f"web-{random.randint(100000000,999999999)}",
            "gameSlug": "",
            "referrer": ""
        }

        try:
            r = requests.post("https://ngl.link/api/submit", 
                            json=payload, 
                            headers=headers, 
                            proxies=proxy_dict, 
                            timeout=12)

            if r.status_code == 200:
                success += 1
                print(f"{Fore.GREEN}[✓] {i:3d}/{amount} | {proxy.split('//')[1][:20]:20} | Sent")
            else:
                failed += 1
                print(f"{Fore.RED}[✗] {i:3d}/{amount} | Failed {r.status_code}")
        except:
            failed += 1
            print(f"{Fore.YELLOW}[!] {i:3d}/{amount} | Proxy Error → Skipping")

        time.sleep(random.uniform(0.4, 1.5))  # delay agak natural

    print(Fore.CYAN + f"\n{'='*50}")
    print(Fore.GREEN + f"SELESAI! Success: {success} | Failed: {failed}")
    print(Fore.CYAN + f"{'='*50}")

# ================== MAIN ==================
banner()
username = input(Fore.WHITE + "Target Username: " + Fore.YELLOW)
message = input(Fore.WHITE + "Pesan Spam: " + Fore.YELLOW)
amount = int(input(Fore.WHITE + "Jumlah Spam: " + Fore.YELLOW))

print(Fore.MAGENTA + "\nStarting spam with proxy rotation...\n")
spam_ngl(username, message, amount)