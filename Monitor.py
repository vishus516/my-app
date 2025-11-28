# cpu_monitor.py
#test A simple CPU usage monitor that alerts when usage exceeds a defined threshold.
import time
import psutil
import os
import unicodedata
from datetime import datetime

THRESHOLD = 80.0   # percent
INTERVAL = 5       # seconds between checks

def alert(msg):
    # Simple console + placeholder for email/pager integration
    print(f"[ALERT] {datetime.now().isoformat()} - {msg}")
    # Example: send email/sns/slack here

def main():
    while True:
        cpu = psutil.cpu_percent(interval=1)   # blocking 1s average.
        if cpu > THRESHOLD:
            alert(f"CPU usage high real: {cpu}%")
        time.sleep(INTERVAL - 1)

if __name__ == "__main__":
    main()
