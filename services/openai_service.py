import os
import random

from openai import OpenAI
from dotenv import load_dotenv

from utils.logger import log_event

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

FALLBACK_QUOTES = [
    "Consistency builds long-term success.",
    "Small progress each day leads to big results.",
    "Stay focused and trust the process.",
    "Discipline creates lasting achievement.",
    "Keep going, even when progress feels slow."
]

def generate_motivational_quote():
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You generate short professional motivational quotes for workplace productivity."
                },
                {
                    "role": "user",
                    "content": "Generate one motivational quote."
                }
            ],
            max_tokens=50
        )

        quote = response.choices[0].message.content.strip()

        log_event(
            event_type="AI_SERVICE",
            task_name="OpenAI Quote Generation",
            status="SUCCESS",
            details="GPT-generated quote returned successfully"
        )

        return quote

    except Exception as error:
        fallback_quote = random.choice(FALLBACK_QUOTES)

        log_event(
            event_type="AI_SERVICE",
            task_name="OpenAI Quote Generation",
            status="FALLBACK",
            details=str(error)
        )

        return fallback_quote