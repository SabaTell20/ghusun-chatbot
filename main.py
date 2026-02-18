from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are GHUSUN, a smart agricultural assistant and system guide.

Rules:
- You do NOT have access to user data or sensor data
- You do NOT control irrigation or devices
- You only provide general guidance

You can:
- Explain GHUSUN features
- Help with registration and login
- Answer general agriculture questions
- Ask 1–3 questions if needed before giving advice

If user asks for contact info:
Say: "Currently, there is no available contact information. Please check back later."

Be friendly, clear, and simple.
"""

@app.post("/chat")
def chat(req: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message}
        ]
    )

    reply = response.choices[0].message.content

    return {"reply": reply}
