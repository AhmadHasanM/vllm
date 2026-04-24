from openai import OpenAI

client = OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1",
)

print("=== Contoh 1: System prompt sebagai HR Expert ===")

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    messages=[
        {
            "role": "system",
            "content": "Kamu adalah HR Expert yang ahli dalam employee promotion. "
                       "Jawab selalu dalam Bahasa Indonesia, singkat dan profesional."
        },
        {
            "role": "user",
            "content": "Faktor apa yang paling penting dalam menilai karyawan untuk promosi?"
        },
    ],
    max_tokens=150,
    temperature=0.7,
)
print(response.choices[0].message.content)

print("\n=== Contoh 2: Multi-turn conversation ===")

# Simulasi percakapan bertahap
conversation_history = [
    {
        "role": "system",
        "content": "Kamu adalah asisten HR yang membantu analisis promosi karyawan."
    }
]

# Giliran pertama
conversation_history.append({
    "role": "user",
    "content": "Siapa nama kamu?"
})

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    messages=conversation_history,
    max_tokens=80,
    temperature=0.7,
)

assistant_reply = response.choices[0].message.content
print(f"User    : Siapa nama kamu?")
print(f"Assistant: {assistant_reply}")

# Simpan jawaban model ke history
conversation_history.append({
    "role": "assistant",
    "content": assistant_reply
})

# Giliran kedua — model ingat percakapan sebelumnya
conversation_history.append({
    "role": "user",
    "content": "Bisa bantu saya menentukan apakah Andi layak dipromosikan? "
               "KPI score-nya 92, attendance 96%, dan sudah 3 tahun di posisi yang sama."
})

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    messages=conversation_history,
    max_tokens=150,
    temperature=0.7,
)

assistant_reply2 = response.choices[0].message.content
print(f"\nUser    : Bisa bantu analisis promosi Andi?")
print(f"Assistant: {assistant_reply2}")