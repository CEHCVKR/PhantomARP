# PhantomARP

> ⚠️ Advanced ARP Spoofing Tool for Local Network Hijacking  
> **Author**: CHINNAPAREDDY VENKATA KARTHIK REDDY  
> **For Educational and Ethical Research Purposes Only**

**PhantomARP** is a multi-threaded ARP spoofing tool that automatically scans your local network, discovers active devices, and continuously poisons their ARP tables to redirect traffic to your system (typically for packet inspection or filtering).

---

## 📌 Features

- 🧠 Automatic ARP scan of entire subnet (`/24`)
- 👻 Continuous ARP spoofing of all discovered devices
- 🧼 ARP table restoration on script exit (Ctrl+C)
- 🔄 Real-time scanning every 5 seconds to find and re-spoof new devices
- 🔒 Thread-safe and stable performance with `threading` and `Event`

---

## ⚙️ Requirements

- Python 3.x
- `scapy`

Install dependencies:

```bash
pip install scapy
```

> 🔐 Must be run with **root/admin privileges** to allow raw socket operations.

---

## 🛠️ Configuration

Edit these variables in `main.py` before running:

```python
laptop_ip = "192.168.31.248"       # IP of the device you want to impersonate
pc_mac = "00:2F:A7:E3:70:8A"        # MAC of your attacker device (PC)
target_range = "192.168.31.1/24"   # Subnet to scan and attack
```

---

## 🚀 Usage

```bash
sudo python3 main.py
```

### Output Example

```
[*] Scan complete. Found 5 devices.
[!] Re-spoofed 192.168.31.10 immediately after scan
[!] Re-spoofed 192.168.31.11 immediately after scan
[!] Ctrl+C detected! Cleaning up...
[*] ARP tables restored.
```

---

## 📁 File Description

| File       | Description                                 |
|------------|---------------------------------------------|
| `main.py`  | Core ARP spoofing and scanning logic        |
| `README.md`| You are reading it now                      |

---

## ⚠️ Disclaimer

This tool is intended **only for use in networks you own or are authorized to test**.  
**Unauthorized usage** is a **criminal offense** under most cybercrime laws.

---

## 🧠 How It Works

1. Scans the entire subnet for devices (excluding the spoofed IP)
2. Sends **forged ARP replies** to tell each device:  
   `192.168.31.248 is at 00:2F:A7:E3:70:8A`
3. Devices start sending traffic to your PC
4. Rescans every 5 seconds and re-spoofs newly discovered hosts
5. On exit (`Ctrl+C`), it restores the correct ARP mapping to clean up

---

## 📬 Contact

- 📧 Email: [22bq1a4720@gmail.com](mailto:22bq1a4720@gmail.com)
- 🌐 GitHub: [@CEHCVKR](https://github.com/CEHCVKR)
- 💼 LinkedIn: [@cvkr](https://linkedin.com/in/cvkr)

---

## 🔐 License

This project is for **educational and ethical research** only.  
Use responsibly. Abuse of this tool is strictly discouraged.
