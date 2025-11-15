import tkinter as tk
import psutil
import threading
import time
import datetime

# --- Extra Functions Added ---
# 1. Calculate network speed (upload/download per second)
# 2. Show CPU usage
# 3. Show memory usage
# 4. Show system uptime
# 5. Refresh every 2 seconds in background thread

prev_sent = psutil.net_io_counters().bytes_sent
prev_recv = psutil.net_io_counters().bytes_recv


def get_network_speed():
    global prev_sent, prev_recv
    counters = psutil.net_io_counters()
    sent_speed = counters.bytes_sent - prev_sent
    recv_speed = counters.bytes_recv - prev_recv
    prev_sent, prev_recv = counters.bytes_sent, counters.bytes_recv
    return sent_speed, recv_speed


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used, mem.total


def get_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    return str(uptime).split('.')[0]  # remove microseconds


def update_stats():
    while True:
        # network
        net = psutil.net_io_counters()
        sent_speed, recv_speed = get_network_speed()

        # cpu
        cpu = get_cpu_usage()

        # memory
        mem_percent, mem_used, mem_total = get_memory_usage()

        # uptime
        up = get_uptime()

        # update ui
        text = (
            f"Bytes Sent: {net.bytes_sent}\n"
            f"Bytes Received: {net.bytes_recv}\n\n"
            f"Upload Speed: {sent_speed} B/s\n"
            f"Download Speed: {recv_speed} B/s\n\n"
            f"CPU Usage: {cpu}%\n"
            f"Memory Usage: {mem_percent}%  ({mem_used / (1024**3):.2f} GB / {mem_total / (1024**3):.2f} GB)\n\n"
            f"System Uptime: {up}"
        )
        stats_label.config(text=text)

        time.sleep(2)


# --- UI Setup ---
app = tk.Tk()
app.title("Network & System Monitor")

stats_label = tk.Label(app, text="Loading system stats...", font=("Helvetica", 14), justify="left")
stats_label.pack(pady=20)

# Background thread
threading.Thread(target=update_stats, daemon=True).start()

app.mainloop()
