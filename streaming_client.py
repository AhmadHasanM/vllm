from openai import OpenAI
import time

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"          # vLLM tidak butuh API key
)

messages = [
    {"role": "system", "content": "Kamu adalah HR Expert yang ahli dalam employee promotion. Jawab selalu dalam Bahasa Indonesia, singkat dan profesional."},
    {"role": "user", "content": "Faktor apa yang paling penting dalam menilai karyawan untuk promosi?"}
]

print("Assistant: ", end="", flush=True)

stream = client.chat.completions.create(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    messages=messages,
    temperature=0.6,
    max_tokens=300,
    stream=True,                    # ← Ini kuncinya untuk streaming
    stream_options={"include_usage": True}
)

full_response = ""
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        print(content, end="", flush=True)
        full_response += content
    # Optional: bisa cek usage di chunk terakhir

print("\n\n=== Streaming selesai ===")