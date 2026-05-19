from services.openai_service import generate_motivational_quote
from utils.logger import log_event

def summarize_email(email_text):
    """
    Simple GPT-based email summarizer
    """

    summary_prompt = f"""
    Summarize the following email into:
    - Key points
    - Action items
    - Important dates

    Email:
    {email_text}
    """

    try:
        from openai import OpenAI
        import os
        from dotenv import load_dotenv

        load_dotenv()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are an email summarization assistant."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=200
        )

        summary = response.choices[0].message.content.strip()

        log_event(
            event_type="EMAIL",
            task_name="Email Summarization",
            status="SUCCESS",
            details="Email summarized successfully"
        )

        return summary
    
    except Exception as e:
        log_event(
            event_type="EMAIL",
            task_name="Email Summarization",
            status="ERROR",
            details=str(e)
        )

        return "Email summarization failed."