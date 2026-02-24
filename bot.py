import socket, os, time, urllib.request, random

# --- CONFIGURATION ---
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#sachaslm" 

# On utilise deux APIs différentes pour la rapidité
API_URLS = [
    f"https://decapi.me/twitch/uptime/{CHAN.replace('#', '')}",
    f"https://api.crunchyroll.moe/twitch/uptime/{CHAN.replace('#', '')}" # Source alternative
]

def send_msg(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\n".encode('utf-8'))

def check_live_multi():
    for url in API_URLS:
        try:
            response = urllib.request.urlopen(url, timeout=2).read().decode('utf-8')
            if "offline" not in response.lower() and "error" not in response.lower():
                return True
        except: continue
    return False

def connect_and_lurk():
    sock = socket.socket()
    sock.settimeout(5)
    try:
        sock.connect(("irc.chat.twitch.tv", 6667))
        sock.send(f"PASS {PASS}\n".encode('utf-8'))
        sock.send(f"NICK {NICK}\n".encode('utf-8'))
        sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
    except: return

    has_sent_initial = False
    start_time = time.time()
    last_check_time = 0

    while time.time() - start_time < 19200: # 5h20
        current_time = time.time()

        # On vérifie toutes les 2 SECONDES au lieu de 5
        if current_time - last_check_time >= 2:
            last_check_time = current_time
            if check_live_multi():
                if not has_sent_initial:
                    # REACTION INSTANTANEE
                    send_msg(sock, "yo")
                    time.sleep(1) # Petit délai pour Wizebot
                    send_msg(sock, "cv ?")
                    has_sent_initial = True
                    print("[!] LIVE DÉTECTÉ ET VALIDÉ")
            else:
                has_sent_initial = False

        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'): sock.send("PONG\n".encode('utf-8'))
        except: continue
        time.sleep(0.5)

if __name__ == "__main__":
    connect_and_lurk()
