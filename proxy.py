#!/usr/bin/env python3

import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import os
import warnings

INPUT = "/storage/emulated/0/Download/cao_proxy/proxy.txt"
VN_OUTPUT = "/storage/emulated/0/Download/cao_proxy/vn.txt"

lock = threading.Lock()
checked = 0
live_count = 0
total = 0

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

def load_proxies():
    if not os.path.exists(INPUT):
        print("❌ Không tìm thấy file proxy.txt")
        exit()

    with open(INPUT, "r") as f:
        proxies = [line.strip() for line in f if ":" in line]

    print(f"📥 Đã tải {len(proxies)} proxy từ file")
    return proxies

def check(proxy, timeout_http=3, timeout_https=3):
    global checked, live_count
    proxy_url = f"http://{proxy}"
    proxies = {"http": proxy_url, "https": proxy_url}
    is_alive = False

    try:
        if requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout_http).status_code == 200:
            is_alive = True
    except:
        pass

    try:
        if requests.get("https://httpbin.org/ip", proxies=proxies, timeout=timeout_https, verify=False).status_code == 200:
            is_alive = True
    except:
        pass

    with lock:
        checked += 1
        if is_alive:
            with open(VN_OUTPUT, "a") as f:
                f.write(proxy + "\n")
            live_count += 1
        print(f"✅ {checked}/{total} | Lưu: {live_count}", end="\r", flush=True)

def scan(proxies, threads=50):
    if os.path.exists(VN_OUTPUT):
        os.remove(VN_OUTPUT)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for proxy in proxies:
            executor.submit(check, proxy)

if __name__ == "__main__":
    print("📂 Đang đọc proxy từ file...")

    proxy_list = load_proxies()

    if not proxy_list:
        print("❌ File proxy trống.")
        exit()

    total = len(proxy_list)

    print(f"🔍 Tổng proxy: {total}")
    print("⚙️ Đang kiểm tra proxy...\n")

    scan(proxy_list)

    print(f"\n✅ Hoàn tất.")
    print(f"📁 Proxy sống lưu vào: {VN_OUTPUT} | Tổng lưu: {live_count}")