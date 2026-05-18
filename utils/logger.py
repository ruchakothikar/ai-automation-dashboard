import csv
import os
from datetime import datetime

LOG_FILE = "logs/automation_logs.csv"

def log_event(event_type, task_name, status, details=""):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.now().isoformat()

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "event_type", "task_name", "status", "details"])

        writer.writerow([timestamp, event_type, task_name, status, details])
        