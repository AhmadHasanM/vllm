# vLLM Chat Template & Streaming Example

Project ini berisi contoh penggunaan vLLM untuk:
- Chat template (format prompt)
- Online streaming inference

## 📂 Struktur File

- `chat_template.py`  
  Berisi contoh penggunaan chat template untuk mengatur format input model.

- `streaming_online.py`  
  Implementasi streaming output dari model secara real-time.

## ⚙️ Cara Menggunakan
- Pastikan di folder vllm
cd ~/Youfolder/vllm

- Buat venv dengan uv
uv venv --python 3.12 --seed

- Aktifkan
source .venv/bin/activate

- Buka terminal 1
docker run --rm \
  --gpus all \
  --ipc=host \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen2.5-0.5B-Instruct \
  --enforce-eager \
  --max-model-len 512 \
  --gpu-memory-utilization 0.6 \
  --dtype float16

- Buka terminal 2
source .venv/bin/activate
python chat_template.py
python streaming_clinet.py
