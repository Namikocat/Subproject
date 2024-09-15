# Stage 1: Build stage
FROM python:3.8-slim AS builder

WORKDIR /app

COPY requirements.txt .

# ติดตั้ง dependencies ใน build stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt -t /app/deps \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Final stage
FROM python:3.8-slim

WORKDIR /app

COPY --from=builder /app/deps /app/deps
COPY app.py app.py
COPY best.pt best.pt

# เพิ่มไลบรารีที่ติดตั้งไว้ใน PYTHONPATH
ENV PYTHONPATH="/app/deps:${PYTHONPATH}"

CMD ["python", "app.py"]
