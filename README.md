# vLLM HR Promotion Assistant — Docker Deployment

vLLM server untuk model Employee Promotion Prediction, dikemas dalam Docker container agar bisa di-deploy ke cloud.

---

## Struktur Folder

```
vllm-docker/
├── Dockerfile              # Instruksi build Docker image
├── docker-compose.yml      # Konfigurasi untuk docker compose
├── app/
│   └── streaming_client.py # Client untuk test query ke server
└── README.md
```

---

## Cara Build dan Jalankan

### 1. Build image

```bash
docker build -t vllm-hr-promotion:latest .
```

### 2. Jalankan container

```bash
docker run --rm \
  --gpus all \
  --ipc=host \
  -p 8000:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm-hr-promotion:latest
```

### 3. Atau pakai Docker Compose (lebih simple)

```bash
docker compose up
```

### 4. Test query ke server (terminal baru)

```bash
python app/streaming_client.py
```

Atau pakai curl:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-0.5B-Instruct",
    "messages": [{"role": "user", "content": "Apa itu employee promotion?"}],
    "max_tokens": 100
  }'
```

---

## Konfigurasi

Parameter model bisa diubah di `docker-compose.yml` bagian `environment` atau langsung di `CMD` pada `Dockerfile`:

| Parameter | Default | Keterangan |
|---|---|---|
| `--model` | Qwen/Qwen2.5-0.5B-Instruct | Model yang dipakai |
| `--enforce-eager` | True | Matikan CUDA Graphs (hemat VRAM) |
| `--max-model-len` | 512 | Maksimal panjang context |
| `--gpu-memory-utilization` | 0.6 | Persentase VRAM yang dipakai |
| `--dtype` | float16 | Presisi model |
| `--port` | 8000 | Port server |

---

## Deploy ke Cloud

### AWS (ECS + ECR)

```bash
# Push image ke ECR
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com
docker tag vllm-hr-promotion:latest <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/vllm-hr-promotion:latest
docker push <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/vllm-hr-promotion:latest
```

### GCP (Cloud Run)

```bash
# Push image ke Google Container Registry
docker tag vllm-hr-promotion:latest gcr.io/<project-id>/vllm-hr-promotion:latest
docker push gcr.io/<project-id>/vllm-hr-promotion:latest
```

---

## Endpoint yang Tersedia

| Endpoint | Method | Keterangan |
|---|---|---|
| `/health` | GET | Cek status server |
| `/v1/models` | GET | List model yang tersedia |
| `/v1/chat/completions` | POST | Chat completion (OpenAI compatible) |
| `/v1/completions` | POST | Text completion |
| `/metrics` | GET | Prometheus metrics |