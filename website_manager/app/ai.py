from openai import OpenAI
import os

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return OpenAI(api_key=api_key)

def summarise_enquiry(message: str) -> str:
    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarise the enquiry briefly."},
            {"role": "user", "content": message},
        ],
    )

    return response.choices[0].message.content.strip()