import tkinter as tk
import psutil
import threading
import time

def update_network_stats():
    while True:
        net_io = psutil.net_io_counters()
        stats_label.config(text=f"Bytes Sent: {net_io.bytes_sent}\nBytes Received: {net_io.bytes_recv}")
        time.sleep(2)  # Update every 2 seconds

app = tk.Tk()
app.title("Network Activity Monitor")

stats_label = tk.Label(app, text="Loading network stats...", font=("Helvetica", 16))
stats_label.pack(pady=20)

# Run the network stats update in a separate thread
threading.Thread(target=update_network_stats, daemon=True).start()

app.mainloop()
