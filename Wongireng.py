import requests, time, random, os
from colorama import init, Fore, Style

init(autoreset=True)

def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            prox = [line.strip() for line in f if line.strip() and "://" in line]
            print(Fore.GREEN + f"Loaded {len(prox)} proxies")
            return prox
    except:
        print(Fore.RED + "proxies.txt tidak ditemukan!")
        return []

proxies = load_proxies()

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + "NGL SPAMMER + PROXY ROTATION")
    print(Fore.YELLOW + "Author: KENAIRFORCES | Improved by Grok\n")

def spam_ngl(username, message, amount):
    success = 0
    for i in range(1, amount + 1):
        if not proxies:
            print(Fore.RED + "Proxy list kosong!")
            break
            
        proxy = random.choice(proxies)
        proxy_dict = {"http": proxy, "https": proxy}

        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36",
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
                            timeout=15)

            if r.status_code == 200:
                success += 1
                print(f"{Fore.GREEN}[✓] {i:3d}/{amount} | Success | {proxy[:35]}")
            else:
                print(f"{Fore.RED}[✗] {i:3d}/{amount} | Failed {r.status_code}")
        except Exception as e:
            print(f"{Fore.YELLOW}[!] {i:3d}/{amount} | Proxy Dead → Skip")

        time.sleep(random.uniform(0.6, 1.8))   # delay lebih natural

    print(Fore.CYAN + f"\nSELESAI! Berhasil: {success}/{amount}")

# Main
banner()
username = input(Fore.WHITE + "Target Username: " + Fore.YELLOW)
message = input(Fore.WHITE + "Pesan: " + Fore.YELLOW)
amount = int(input(Fore.WHITE + "Jumlah: " + Fore.YELLOW))

print(Fore.MAGENTA + "\nMulai spam...\n")
spam_ngl(username, message, amount)
