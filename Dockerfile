
# ใช้ base image ของ Python
FROM python:3.8-slim

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ที่จำเป็นไปยัง working directory
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY best.pt best.pt  # คัดลอกไฟล์โมเดลของคุณไปยัง Docker image

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# รันแอป
CMD ["python", "app.py"]
