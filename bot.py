import socket
import os
import time

# --- CONFIGURATION ---
# Assure-toi que ces noms correspondent à tes "Secrets" GitHub
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#sachaslm" # Nom du streamer d'après ton image
# ---------------------

def send_msg(sock, msg):
    sock.send(f"PRIVMSG {CHAN} :{msg}\n".encode('utf-8'))

def connect_and_lurk():
    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))
    sock.send(f"PASS {PASS}\n".encode('utf-8'))
    sock.send(f"NICK {NICK}\n".encode('utf-8'))
    sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
    
    # Message de confirmation envoyé dans le chat
    # On attend 2 secondes pour laisser la connexion s'établir
    time.sleep(2)
    send_msg(sock, "!myuptime")
    
    print(f"[*] Message envoyé. Connecté au chat de {CHAN}.")
    
    start_time = time.time()
    # Le script tourne pendant 5 heures (18000 secondes)
    while time.time() - start_time < 18000: 
        try:
            resp = sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
        except:
            break
        time.sleep(10)

if __name__ == "__main__":
    connect_and_lurk()
