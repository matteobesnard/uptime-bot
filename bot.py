import socket
import os
import time
import urllib.request

# --- CONFIGURATION ---
# Utilisation des secrets configurés dans GitHub
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#sachaslm" # Nom de la chaîne confirmé sur ton écran
# ---------------------

def send_msg(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\n".encode('utf-8'))

def is_stream_live():
    """Vérifie si le stream est en ligne via DecAPI"""
    try:
        user = CHAN.replace("#", "")
        url = f"https://decapi.me/twitch/uptime/{user}"
        # Timeout de 2 secondes pour ne pas bloquer le script
        response = urllib.request.urlopen(url, timeout=2).read().decode('utf-8')
        return "offline" not in response.lower()
    except:
        return False

def connect_and_lurk():
    sock = socket.socket()
    sock.settimeout(5)
    try:
        sock.connect(("irc.chat.twitch.tv", 6667))
        sock.send(f"PASS {PASS}\n".encode('utf-8'))
        sock.send(f"NICK {NICK}\n".encode('utf-8'))
        sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
        print(f"[*] Connecté en tant que {NICK} sur {CHAN}")
    except Exception as e:
        print(f"[!] Erreur de connexion : {e}")
        return

    has_sent_uptime = False
    start_time = time.time()
    last_check_time = 0

    # Le script tourne pendant 5 heures (limite des serveurs GitHub Actions)
    while time.time() - start_time < 18000:
        current_time = time.time()

        # --- VÉRIFICATION TOUTES LES 5 SECONDES ---
        if current_time - last_check_time >= 5:
            last_check_time = current_time
            if is_stream_live():
                if not has_sent_uptime:
                    print(f"[!] LIVE détecté ! Envoi de !myuptime...")
                    send_msg(sock, "cc, comment tu vas ?")
                    has_sent_uptime = True 
            else:
                if has_sent_uptime:
                    print("[*] Le stream est hors ligne. Reset pour le prochain live.")
                    has_sent_uptime = False 

        # Maintien de la connexion (réponse au PING de Twitch)
        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
        except socket.timeout:
            continue
        except:
            break
        
        time.sleep(0.5)

if __name__ == "__main__":
    connect_and_lurk()
