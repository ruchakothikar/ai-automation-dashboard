from services.openai_service import generate_motivational_quote
from utils.logger import log_event

def get_motivational_quote():
    quote = generate_motivational_quote()

    log_event(
        event_type="AUTOMATION",
        task_name="Motivational Quote Generator",
        status="SUCCESS",
        details=quote
    )

    return quote
