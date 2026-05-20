import pandas as pd

LOG_FILE = "logs/automation_logs.csv"

def load_logs():
    try:
        df = pd.read_csv(LOG_FILE, encoding="latin1")
        return df
    except Exception as e:

        return pd.DataFrame(
            columns=[
                "timestamp",
                "event_type",
                "task_name",
                "status",
                "details"
            ]
        )
    
def get_summary_metrics():
    df = load_logs()

    if df.empty:
        return {
            "total_events": 0,
            "success_count": 0,
            "fallback_count": 0,
            "error_count": 0
        }
    
    return {
        "total_events": len(df),
        "success_count": len(df[df["status"] == "SUCCESS"]),
        "fallback_count": len(df[df["status"] == "FALLBACK"]),
        "error_count": len(df[df["status"] == "ERROR"])
    }