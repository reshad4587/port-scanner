import socket
import concurrent.futures
from datetime import datetime
import tkinter as tk
import threading

scan_running = False

def scan_port(target, port):
    global scan_running
    if not scan_running:
        return
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass

def scan_ports(target, root):
    print("-" * 50)
    print(f"Scanning target: {target}")
    print(f"Started scanning at: {str(datetime.now())}")
    print("-" * 50)
    
    global scan_running
    scan_running = True

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in range(1, 65535)]

        for future in concurrent.futures.as_completed(futures):
            if not scan_running:
                break

    scan_running = False
    root.after(10, root.destroy)  # Close the window after the scan is finished

def start_scan(ip_entry, root):
    target = ip_entry.get()
    ip_entry.delete(0, tk.END)
    
    def scan_target():
        scan_ports(target, root)

    # Create a separate thread for the scan
    scan_thread = threading.Thread(target=scan_target)
    scan_thread.start()
    
def on_closing(root):
    global scan_running
    if scan_running:
        scan_running = False

def create_gui():
    root = tk.Tk()
    root.title("Port Scanner")

    label = tk.Label(root, text="Enter IP address:")
    label.pack()
    ip_entry = tk.Entry(root)
    ip_entry.pack()

    scan_button = tk.Button(root, text="Start Scan", command=lambda: start_scan(ip_entry, root))
    scan_button.pack()
    
    ip_entry.bind("<Return>", lambda event: start_scan(ip_entry, root))

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    root.mainloop()

def main():
    create_gui()

if __name__ == "__main__":
    main()
