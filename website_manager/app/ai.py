from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarise_enquiry(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarise the enquiry briefly."},
            {"role": "user", "content": message},
        ],
    )

    return response.choices[0].message.content.strip()

