import os
from typing import List, Dict
from dotenv import load_dotenv


from groq import Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY_78060"),
)


class BaseAgent:
    def __init__(self, name: str, system_prompt: str, model: str = "llama-3.3-70b-versatile"):
        self.name = name
        self.system_prompt = {"role": "system", "content": system_prompt.strip()}
        self.model = model
        self.history: List[Dict[str, str]] = [self.system_prompt]

    def respond(self, user_msg: str) -> str:
        self.history.append({"role": "user", "content": user_msg})

        response = client.chat.completions.create(
            model=self.model,
            messages=self.history,
            temperature=0.7,
            max_tokens=200
        )

        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply

