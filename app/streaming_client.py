from openai import OpenAI
import time
import sys

BASE_URL = "http://localhost:8000/v1"
MODEL    = "Qwen/Qwen2.5-0.5B-Instruct"

client = OpenAI(base_url=BASE_URL, api_key="EMPTY")

SYSTEM_PROMPT = """Kamu adalah HR AI Assistant yang ahli dalam:
- Analisis performa karyawan
- Rekomendasi promosi berdasarkan data
- Evaluasi KPI, attendance, dan soft skill

Selalu jawab dalam Bahasa Indonesia, profesional, dan berbasis data."""

def stream_chat(messages: list, max_tokens: int = 200) -> str:
    """
    Kirim messages ke vLLM server dan tampilkan response secara streaming.
    Return: full response sebagai string
    """
    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.6,
            max_tokens=max_tokens,
            stream=True,
            stream_options={"include_usage": True}
        )

        full_response = ""
        print("Assistant: ", end="", flush=True)

        for chunk in stream:
            # Ambil usage info di chunk terakhir
            if hasattr(chunk, "usage") and chunk.usage:
                total_tokens = chunk.usage.total_tokens

            # Print token per token
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content

        print()  # newline setelah selesai
        return full_response

    except Exception as e:
        print(f"\n[ERROR] Gagal connect ke server: {e}")
        print("Pastikan vLLM server sudah jalan dengan: vllm serve ...")
        sys.exit(1)

def run_conversation():
    """Jalankan multi-turn conversation dengan HR AI."""

    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # ── Skenario 1: Pertanyaan umum ──
    print("\n" + "="*60)
    print("SKENARIO 1 — Pertanyaan Umum Promosi")
    print("="*60)

    pertanyaan_1 = "Faktor apa yang paling penting dalam menilai karyawan untuk promosi?"
    print(f"User: {pertanyaan_1}")

    conversation_history.append({"role": "user", "content": pertanyaan_1})
    reply_1 = stream_chat(conversation_history)
    conversation_history.append({"role": "assistant", "content": reply_1})

    # ── Skenario 2: Analisis karyawan spesifik ──
    print("\n" + "="*60)
    print("SKENARIO 2 — Analisis Karyawan Spesifik")
    print("="*60)

    data_karyawan = """
    Tolong analisis apakah karyawan berikut layak dipromosikan:
    - Nama       : Andi Santoso
    - Jabatan    : Senior Specialist
    - KPI Score  : 92/100
    - Attendance : 96%
    - Lama di posisi saat ini: 3 tahun
    - Awards     : 2 penghargaan tahun ini
    - Feedback   : Kepemimpinan kuat, inisiatif tinggi
    """
    print(f"User: {data_karyawan.strip()}")

    conversation_history.append({"role": "user", "content": data_karyawan})
    reply_2 = stream_chat(conversation_history)
    conversation_history.append({"role": "assistant", "content": reply_2})

    # ── Skenario 3: Follow-up question ──
    print("\n" + "="*60)
    print("SKENARIO 3 — Follow-up Question")
    print("="*60)

    followup = "Berdasarkan analisis tadi, apa yang sebaiknya Andi persiapkan sebelum proses promosi dimulai?"
    print(f"User: {followup}")

    conversation_history.append({"role": "user", "content": followup})
    reply_3 = stream_chat(conversation_history)

    print("\n" + "="*60)
    print("Conversation selesai.")
    print("="*60)

if __name__ == "__main__":
    print("="*60)
    print("  HR AI Assistant — vLLM Streaming Client")
    print(f"  Server  : {BASE_URL}")
    print(f"  Model   : {MODEL}")
    print("="*60)

    # Cek dulu apakah server sudah jalan
    try:
        models = client.models.list()
        print(f"  Status  : Server OK ✓")
        print(f"  Models  : {[m.id for m in models.data]}")
    except Exception:
        print("  Status  : Server OFFLINE ✗")
        print("  Jalankan dulu: vllm serve Qwen/Qwen2.5-0.5B-Instruct --enforce-eager ...")
        sys.exit(1)

    run_conversation()