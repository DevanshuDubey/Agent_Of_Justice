from groq import Groq  # Or Hugging Face client if you're using HF
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_text(long_text, model="mixtral-8x7b-32768"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a legal assistant summarizing lengthy case descriptions."},
                {"role": "user", "content": f"Summarize this legal case in 300–500 words:\n\n{long_text}"}
            ],
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return long_text[:2000]  # fallback: truncate
