# ==============================================================================
# VigilanteSilentiumShield - Judicium in Silentio, Scutum in Umbra
# ==============================================================================
#
# SYSTEM: VIGILANTE INQUISITOR
# ROLE: ADVANCED RECON & AUTH AUDIT FRAMEWORK
# ARCHITECTURE: ASYNCIO (OPTIMIZED FOR LENOVO L412)
#
# ==============================================================================

import asyncio
import argparse
import socket
import sys
import random
import time
from datetime import datetime

# Check for required modules gracefully
try:
    import aiohttp
    import requests
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] MISSING LIBRARIES. RUN: pip install aiohttp requests colorama")
    sys.exit()

# [!] CONFIGURATION: HUMANIZATION PROTOCOL
# Manipulasi ritme paket untuk menghindari deteksi pola bot.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

# COLORS
C = Fore.CYAN
G = Fore.GREEN
R = Fore.RED
Y = Fore.YELLOW
W = Style.RESET_ALL

def print_banner():
    print(f"""{C}
    █ █ █ ▄▀▄ █ █ █ ▄▀▀ █ ▀█▀ ▄▀▄ █▀▄
    ▀▄▀ █ █▄█ █ █▄▀ ░▀▄ █  █  █▄█ █▀▄
    {W}:: JUDICIUM IN SILENTIO, SCUTUM IN UMBRA ::
    :: TARGET: {sys.argv[-1] if len(sys.argv) > 1 else 'UNKNOWN'} ::{W}
    """)

# --- MODULE 1: STEALTH PORT RECON (Async Logic) ---
async def scan_port(ip, port):
    try:
        # HUMANIZE: Random Jitter (0.1s - 0.5s) to break signature based detection
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        conn = asyncio.open_connection(ip, port)
        try:
            reader, writer = await asyncio.wait_for(conn, timeout=1.5)
            
            # Banner Grabbing (Polite Check)
            try:
                writer.write(b'HEAD / HTTP/1.0\r\n\r\n')
                await writer.drain()
                data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                banner = data.decode('utf-8', errors='ignore').strip().split('\n')[0][:40]
            except:
                banner = "Silent Service"
                
            print(f"{G}[+] OPEN | Port: {port:<5} | Info: {banner}{W}")
            writer.close()
            await writer.wait_closed()
        except (asyncio.TimeoutError, ConnectionRefusedError):
            pass
    except Exception:
        pass

async def run_recon(target):
    print(f"\n{Y}[*] INITIATING STEALTH RECON...{W}")
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"{R}[!] DNS RESOLUTION FAILED.{W}")
        return

    print(f"{Y}[*] TARGET IP: {ip} (Local/NAT){W}")
    
    # Common Attack Surface Ports
    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 3306, 3389, 5432, 8080, 8443]
    
    tasks = [scan_port(ip, p) for p in ports]
    await asyncio.gather(*tasks)

# --- MODULE 2: PASSIVE OSINT (CRT.SH Integration) ---
def run_osint(target):
    print(f"\n{Y}[*] RUNNING PASSIVE OSINT (CERTIFICATE SEARCH){W}")
    url = f"https://crt.sh/?q={target}&output=json"
    try:
        ua = random.choice(USER_AGENTS)
        req = requests.get(url, timeout=15, headers={'User-Agent': ua})
        
        if req.status_code == 200:
            data = req.json()
            subs = set(entry['name_value'] for entry in data)
            
            print(f"{G}[+] SUBDOMAINS FOUND: {len(subs)}{W}")
            for s in list(subs)[:15]: # Limit output for readability
                print(f"   > {s}")
            if len(subs) > 15: print(f"   ... ({len(subs)-15} hidden)")
        else:
            print(f"{R}[!] API STATUS: {req.status_code}{W}")
    except Exception as e:
        print(f"{R}[!] OSINT ERROR: {e}{W}")

# --- MODULE 3: AUTH AUDIT SIMULATION (Targeted) ---
async def auth_worker(session, url, user, password):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    payload = {'username': user, 'password': password, 'submit': 'Login'}
    
    try:
        # Slow Attack Mode (Low noise)
        await asyncio.sleep(random.uniform(0.5, 2.0))
        async with session.post(url, data=payload, headers=headers) as resp:
            # Simple heuristic detection
            if resp.status_code in [200, 302]:
                print(f"{C}[TEST] {user}:{password} -> CODE: {resp.status_code}{W}")
    except:
        pass

async def run_audit(target_domain):
    target_url = f"http://{target_domain}/login" # Assumption
    print(f"\n{Y}[*] AUDIT SIMULATION: {target_url}{W}")
    
    # Default credentials check
    creds = [("admin", "admin"), ("admin", "password"), ("root", "toor"), ("user", "123456")]
    
    async with aiohttp.ClientSession() as session:
        tasks = [auth_worker(session, target_url, u, p) for u, p in creds]
        await asyncio.gather(*tasks)

# --- CONTROLLER ---
def main():
    print_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Target Domain or IP", required=True)
    parser.add_argument("--mode", choices=['recon', 'osint', 'audit', 'full'], default='full')
    args = parser.parse_args()

    if args.mode in ['recon', 'full']:
        asyncio.run(run_recon(args.target))
    
    if args.mode in ['osint', 'full']:
        run_osint(args.target)
        
    if args.mode in ['audit', 'full']:
        asyncio.run(run_audit(args.target))

    print(f"\n{C}[*] OPERATION COMPLETE. SYSTEM STANDBY.{W}")

if __name__ == "__main__":
    main()
