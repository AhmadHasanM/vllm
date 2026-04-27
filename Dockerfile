FROM vllm/vllm-openai:latest

# Metadata
LABEL maintainer="Ahmad Hasan"
LABEL description="vLLM server untuk HR Employee Promotion Prediction"
LABEL version="1.0"

# Working directory
WORKDIR /app

# Copy client (opsional untuk testing)
COPY app/streaming_client.py /app/streaming_client.py

# Install dependency tambahan
RUN pip install --no-cache-dir openai

# Expose port
EXPOSE 8000

# Default environment (bisa dioverride)
ENV MODEL_NAME=Qwen/Qwen2.5-0.5B-Instruct
ENV GPU_MEMORY_UTILIZATION=0.6
ENV MAX_MODEL_LEN=512
ENV DTYPE=float16

# Jalankan vLLM server
CMD python -m vllm.entrypoints.openai.api_server \
    --model $MODEL_NAME \
    --enforce-eager \
    --max-model-len $MAX_MODEL_LEN \
    --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
    --dtype $DTYPE \
    --host 0.0.0.0 \
    --port 8000