<h1 align="center">⚔️ Hardwarica-C2</h1>
<p align="center">
  <b>A Stealthy Multi-Victim Discord-Based Command & Control Framework</b><br>
  <i>Built for Red Teamers, by Red Teamers.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Discord-C2%20Implant-blue?logo=discord&style=flat-square">
  <img src="https://img.shields.io/badge/Stealth-Enabled-green?style=flat-square">
  <img src="https://img.shields.io/badge/Python-3.x-yellow?logo=python&style=flat-square">
</p>

---

## 🚀 Overview

**Hardwarica-C2** is a Python-based, modular, and multi-victim **Discord Command & Control implant** designed for adversary simulation, ethical red teaming, and offensive cyber research.

Each infected host automatically creates its own private channel inside your Discord server—giving you per-victim control and persistent access.

---

## 🔥 Features

| Command           | Description                                                   |
|------------------|---------------------------------------------------------------|
| `!getinfo`        | Gather system hostname, OS, and IP                            |
| `!screenshot`     | Take and upload a screenshot                                  |
| `!clipboard`      | Exfiltrate clipboard content                                  |
| `!camera`         | Take a snapshot from the webcam                               |
| `!keylogger`      | Start background keylogging                                   |
| `!dumpkeys`       | Dump and clear collected keystrokes                           |
| `!stealcreds`     | Exfiltrate Chrome's Local State file for credential theft     |
| `!revshell`       | Reverse shell connection to attacker (Netcat)                 |
| `!persist`        | Task Scheduler persistence (no admin needed)                  |
| `!winpersist`     | Registry-based persistence (`HKCU\\Run`)                      |
| `!selfdestruct`   | Delete implant from disk and exit                             |
| `!upload <path>`  | Upload a file from victim to Discord                          |
| `!download <name>`| Save a file from Discord to the victim                        |
| `!listdir <path>` | List directory contents                                       |

---

## 🧠 Architecture

- **🎯 Discord C2:** Each victim gets a private channel on your server.
- **🔐 Modular Commands:** Easy to extend and modify.
- **🕵️ Stealth Mode:** No GUI, runs silently in background.
- **💾 Persistence:** Survives reboots via Task Scheduler or Registry key.
- **⚡ Fast Deployment:** Works out-of-the-box with Python 3.x.

---

## ⚙️ Setup Instructions

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Configure the bot token and server ID
# Edit these lines in hardwarica_c2_multivictim.py
TOKEN = "your_discord_bot_token"
GUILD_ID = your_discord_server_id

# Step 3: Start listener for reverse shell (on attacker's machine)
nc -lvnp 4444

# Step 4: Run implant on target
python hardwarica_c2_multivictim.py
```


## 🛰️ MITRE ATT&CK Mapping
| Tactic             | Technique (ID)                                               |
|-------------------|--------------------------------------------------------------|
| Credential Access  | Chrome Local State Stealer (T1555.003)                      |
| Execution          | Reverse Shell (T1059.003)                                    |
| Persistence        | Registry Run Key (T1547.001), Task Scheduler (T1053.005)    |
| Collection         | Screenshot (T1113), Clipboard (T1115), Keylogging (T1056.001)|
| Exfiltration       | File Upload/Download (T1041)                                |


⚠️ Disclaimer
This tool is intended strictly for educational purposes and authorized testing.
Any misuse is solely the responsibility of the user.
The author assumes no liability for unauthorized use.

👤 Author
Suyash Shrestha
aka blackrabbitx_x

📺 Coming Soon
🎥 Video walkthrough
