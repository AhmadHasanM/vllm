FROM vllm/vllm-openai:latest

WORKDIR /app

COPY app/streaming_client.py /app/streaming_client.py

RUN pip install --no-cache-dir openai

EXPOSE 8000

# ❗ ENV tetap boleh (optional)
ENV MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
ENV GPU_MEMORY_UTILIZATION=0.6
ENV MAX_MODEL_LEN=512
ENV DTYPE=float16

# ✅ HANYA ARGUMENT ke vllm serve
CMD ["Qwen/Qwen2.5-0.5B-Instruct",
     "--enforce-eager",
     "--max-model-len", "1024",
     "--gpu-memory-utilization", "0.6",
     "--dtype", "float16",
     "--host", "0.0.0.0",
     "--port", "8000"]