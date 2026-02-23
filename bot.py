import socket
import os
import time

# --- CONFIGURATION ---
NICK = os.getenv("TWITCH_NAME")
PASS = os.getenv("TWITCH_TOKEN")
CHAN = "#SachaSLM" # <--- METS LE NOM DU STREAMER ICI (garde le #)
# ---------------------

def connect_and_lurk():
    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))
    sock.send(f"PASS {PASS}\n".encode('utf-8'))
    sock.send(f"NICK {NICK}\n".encode('utf-8'))
    sock.send(f"JOIN {CHAN}\n".encode('utf-8'))
    
    print(f"[*] Connecté au chat de {CHAN}. Ton uptime grimpe !")
    
    # Le script tourne pendant 5 heures
    start_time = time.time()
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
