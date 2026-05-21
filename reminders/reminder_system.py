import json
from datetime import datetime, timedelta
from email_system.email_sender import send_email

from utils.logger import log_event

REMINDER_FILE = "reminders/events.json"

def add_event(title, date_str, email=None, reminder_enabled=False):
    """
    Store an event (format: YYYY-MM-DD)
    """
    try:
        try:
            with open(REMINDER_FILE, "r") as f:
                events = json.load(f)
        except:
            events = []

        events.append({
            "title": title,
            "date": date_str,
            "email": email,
            "reminder_enabled": reminder_enabled,
            "reminder_sent": False
        })

        with open(REMINDER_FILE, "w") as f:
            json.dump(events, f, indent=4)

        log_event(
            event_type="REMINDER",
            task_name="Add Event",
            status="SUCCESS",
            details=f"Event added: {title}"
        )

        return "Event added successfully."
    
    except Exception as e:
        log_event(
            event_type="REMINDER",
            task_name="Add Event",
            status="ERROR",
            details=str(e)
        )

        return "Failed to add event."
    
def check_reminders():
    """
    Check for events happening tomorrow and return reminders
    """
    try:
        try:
            with open(REMINDER_FILE, "r") as f:
                events = json.load(f)
        except:
            return []
        
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

        reminders = []

        for event in events:
            if event["date"] == tomorrow:
                reminders.append(event)

                log_event(
                    event_type="REMINDER",
                    task_name="Trigger Reminder",
                    status="SUCCESS",
                    details=f"Reminder triggered for {event['title']}"
                )

        return reminders
    
    except Exception as e:
        log_event(
            event_type="REMINDER",
            task_name="Check Reminders",
            status="ERROR",
            details=str(e)
    )
        
    return []

def delete_event(title, date_str):
    try:
        try:
            with open(REMINDER_FILE, "r") as f:
                events = json.load(f)
        except:
            return "No events found."
        
        updated_events = [
            e for e in events
            if not (e["title"] == title and e["date"] == date_str)
        ]

        with open(REMINDER_FILE, "w") as f:
            json.dump(updated_events, f, indent=4)

        log_event(
            event_type="REMINDER",
            task_name="Delete Event",
            status="SUCCESS",
            details=f"Deleted event: {title}"
        )

        return "Event deleted successfully."
    
    except Exception as e:
        log_event(
            event_type="REMINDER",
            task_name="Delete Event",
            status="ERROR",
            details=str(e)
        )

        return "Failed to delete event."
    
def edit_event(
    old_title,
    old_date,
    new_title,
    new_date,
    reminder_enabled=False,
    email=None
):
    try:
        try:
            with open(REMINDER_FILE, "r") as f:
                events = json.load(f)
        except:
            return "No events found."
        
        for event in events:
            if event["title"] == old_title and event["date"] == old_date:

                event["title"] = new_title
                event["date"] = new_date

                event["reminder_enabled"] = reminder_enabled

                if reminder_enabled:
                    event["email"] = email
                else:
                    event["email"] = None

                event["reminder_sent"] = False

        with open(REMINDER_FILE, "w") as f:
            json.dump(events, f, indent=4)

        log_event(
            event_type="REMINDER",
            task_name="Edit Event",
            status="SUCCESS",
            details=f"Edited event: {old_title}"
        )

        return "Event updated successfully."
    
    except Exception as e:
        log_event(
            event_type="REMINDER",
            task_name="Edit Event",
            status="ERROR",
            details=str(e)
        )

        return "Failed to update event."
    
def get_all_events():
    try:
        try:
            with open(REMINDER_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    except:
        return []
    
def process_reminders():
    try:
        with open(REMINDER_FILE, "r") as f:
            events = json.load(f)

    except:
        return
    
    today = datetime.now().date()
    updated = False

    for event in events:

        if not event.get("reminder_enabled", False):
            continue

        if event.get("reminder_sent", False):
            continue

        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        days_left = (event_date - today).days

        if 0 <= days_left <= 5:

            send_email(
                subject=f"Reminder: {event['title']}",
                body=f"Event '{event['title']}' is in {days_left} day(s) on {event['date']}.",
                to_email=event["email"]
            )

            event["reminder_sent"] = True
            updated = True

    if updated:
        with open(REMINDER_FILE, "w") as f:
            json.dump(events, f, indent=4)