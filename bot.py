import socket
import os
import time

# --- CONFIGURATION ---
# Changement effectué : on utilise TWITCH_NAME comme demandé
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#sachaslm" 
# ---------------------

def send_msg(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\n".encode('utf-8'))

def connect_and_lurk():
    sock = socket.socket()
    # On force un timeout pour éviter que le script reste bloqué
    sock.settimeout(30)
    try:
        sock.connect(("irc.chat.twitch.tv", 6667))
        sock.send(f"PASS {PASS}\n".encode('utf-8'))
        sock.send(f"NICK {NICK}\n".encode('utf-8'))
        sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
        
        # Petit délai pour laisser Twitch traiter la connexion
        time.sleep(3)
        send_msg(sock, "!myuptime")
        print(f"[*] Connecté en tant que {NICK} sur {CHAN}")
        
    except Exception as e:
        print(f"[!] Erreur de connexion : {e}")
        return

    start_time = time.time()
    # Le script tourne pendant 5 heures
    while time.time() - start_time < 18000: 
        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
        except socket.timeout:
            continue
        except:
            break
        time.sleep(2)

if __name__ == "__main__":
    connect_and_lurk()
