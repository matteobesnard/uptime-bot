import socket, os, time, urllib.request, random

# --- CONFIGURATION ---
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#sachaslm" 

# Ta liste exacte d'alias
COMMAND_ALIASES = [
    "!don", "!ytb", "!wishlist", "!twitter", "!6040", "!tracker", 
    "!tiktok", "!prime", "!subgoals", "!sub", "!maxesport", "!insta", 
    "!mouse", "!setup", "!follow", "!sens", "!ecran", "!discord", 
    "!clavier", "!reseaux", "!res", "!casque", "!bureau"
]

# Dictionnaire des sources pour identifier la plus rapide
API_SOURCES = {
    "DecAPI": f"https://decapi.me/twitch/uptime/{CHAN.replace('#', '')}",
    "TwitchCenter": f"https://twitch.center/customapi/uptime?user={CHAN.replace('#', '')}"
}

def send_msg(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\n".encode('utf-8'))

def check_live_status():
    """Retourne le nom de l'API qui détecte le live en premier."""
    for name, url in API_SOURCES.items():
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=2).read().decode('utf-8')
            if "offline" not in res.lower() and "not live" not in res.lower() and "error" not in res.lower():
                return name
        except: continue
    return None

def connect_and_run():
    sock = socket.socket()
    sock.settimeout(5)
    try:
        sock.connect(("irc.chat.twitch.tv", 6667))
        sock.send(f"PASS {PASS}\n".encode('utf-8'))
        sock.send(f"NICK {NICK}\n".encode('utf-8'))
        sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
        print("[*] Bot connecté et en attente du live...")
    except: return

    is_live_detected = False
    live_start_time = 0
    sent_5s_msg = False
    sent_1m_msg = False
    
    start_run = time.time()
    last_check = 0
    last_activity = 0
    
    while time.time() - start_run < 19200: # 5h20 d'uptime par session GitHub
        now = time.time()

        # Polling toutes les 1 SECONDE pour une réactivité maximale
        if now - last_check >= 1:
            last_check = now
            api_name = check_live_status()
            
            if api_name:
                if not is_live_detected:
                    print(f"[!] LIVE DÉTECTÉ par {api_name} ! Lancement du protocole timing.")
                    is_live_detected = True
                    live_start_time = now
                
                # Gestion des délais demandés
                elapsed = now - live_start_time
                
                # 1. Premier message après 5 secondes
                if elapsed >= 5 and not sent_5s_msg:
                    send_msg(sock, "yo, tu vas bien ?")
                    print("[>] Message de 5s envoyé (cc)")
                    sent_5s_msg = True
                
                # 2. Deuxième message après 1 minute (60s)
                if elapsed >= 60 and not sent_1m_msg:
                    send_msg(sock, "!myuptime")
                    print("[>] Message de 1min envoyé (!myuptime)")
                    sent_1m_msg = True
                    last_activity = now # On commence le cycle des alias après ce message
                
                # 3. Maintien avec les alias (toutes les 45-90 min)
                if sent_1m_msg and (now - last_activity >= random.randint(2700, 5400)):
                    msg = random.choice(COMMAND_ALIASES)
                    send_msg(sock, msg)
                    print(f"[>] Alias de routine envoyé : {msg}")
                    last_activity = now
            else:
                if is_live_detected:
                    print("[i] Le stream semble être fini.")
                is_live_detected = False
                sent_5s_msg = False
                sent_1m_msg = False

        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'): sock.send("PONG\n".encode('utf-8'))
        except: pass
        time.sleep(0.1)

if __name__ == "__main__":
    connect_and_run()
