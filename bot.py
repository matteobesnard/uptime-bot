import socket, os, time, urllib.request, random

# --- CONFIGURATION ---
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#sachaslm" 

# Ta liste exacte de commandes pour une discrétion totale
COMMAND_ALIASES = [
    "!don", "!ytb", "!wishlist", "!twitter", "!6040", "!tracker", 
    "!tiktok", "!prime", "!subgoals", "!sub", "!maxesport", "!insta", 
    "!mouse", "!setup", "!follow", "!sens", "!ecran", "!discord", 
    "!clavier", "!reseaux", "!res", "!casque", "!bureau"
]

# SOURCES API : DecAPI + TwitchCenter (Ultra-rapide)
API_SOURCES = [
    f"https://decapi.me/twitch/uptime/{CHAN.replace('#', '')}",
    f"https://twitch.center/customapi/uptime?user={CHAN.replace('#', '')}"
]

def send_msg(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\n".encode('utf-8'))

def check_live_status():
    """Vérifie le live sur les sources les plus rapides du marché."""
    for url in API_SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=2).read().decode('utf-8')
            # Si le stream est online, ces APIs renvoient le temps (ex: 1h 2m)
            if "offline" not in res.lower() and "not live" not in res.lower() and "error" not in res.lower():
                return True
        except: continue
    return False

def connect_and_run():
    sock = socket.socket()
    sock.settimeout(5)
    try:
        sock.connect(("irc.chat.twitch.tv", 6667))
        sock.send(f"PASS {PASS}\n".encode('utf-8'))
        sock.send(f"NICK {NICK}\n".encode('utf-8'))
        sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
        print("[*] Connexion établie sur les serveurs Twitch.")
    except: return

    is_live_detected = False
    start_run = time.time()
    last_check = 0
    last_activity = 0
    
    # Durée de 5h20 pour assurer le chevauchement (overlap) sans coupure
    while time.time() - start_run < 19200:
        now = time.time()

        # Polling toutes les 1 SECONDE pour ne rater aucun scan de Wizebot
        if now - last_check >= 1:
            last_check = now
            if check_live_status():
                if not is_live_detected:
                    # VALIDATION IMMEDIATE : On force l'enregistrement auprès de Wizebot
                    send_msg(sock, "cc")
                    time.sleep(1)
                    send_msg(sock, "!myuptime")
                    is_live_detected = True
                    last_activity = now
                
                # Un alias au hasard toutes les 45 à 90 minutes pour le maintien d'uptime
                if now - last_activity >= random.randint(2700, 5400): 
                    msg = random.choice(COMMAND_ALIASES)
                    send_msg(sock, msg)
                    last_activity = now
            else:
                is_live_detected = False

        # Gestion du PING Twitch pour éviter le timeout
        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'): sock.send("PONG\n".encode('utf-8'))
        except: pass
        time.sleep(0.1)

if __name__ == "__main__":
    connect_and_run()
