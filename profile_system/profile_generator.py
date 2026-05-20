import os
from openai import OpenAI
from dotenv import load_dotenv
from utils.logger import log_event

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_profile(name, background):
    prompt = f"""
Create a structured professional profile.

Use EXACTLY this format:

Name: {name}
Occupation: (infer from background)

Profile Summary:
Write 1-2 lines describing the person professionally.

Key Skills:
- List 4-6 relevant skills inferred from background

Traits:
- List 3-4 professional traits

Background Summary:
Briefly rephrase and organize the given background into a clean professional description.

Rules:
- Do NOT repeat the input text verbatim
- Do NOT use long paragraphs
- Keep formatting clean and structured
- Make it look like a professional profile card
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You generate structured professional profiles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )

        profile = response.choices[0].message.content.strip()

        log_event(
            event_type="PROFILE",
            task_name="Profile Generation",
            status="SUCCESS",
            details=f"Generated profile for {name}"
        )

        return profile
    
    except Exception as e:
        log_event(
            event_type="PROFILE",
            task_name="Profile Generation",
            status="ERROR",
            details=str(e)
        )

        return "Profile generation failed."