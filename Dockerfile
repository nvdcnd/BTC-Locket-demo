FROM python:3.13-slim

# HF Spaces chạy container bằng user UID 1000 → tạo sẵn user, tránh permission error
RUN useradd -m -u 1000 user
USER user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cache layer deps: chỉ build lại khi requirements.txt đổi
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy code (backend only — deploy API)
COPY --chown=user . .

# Thư mục persistent của HF Space (bật trong Settings → Persistent storage)
# SQLite ghi vào đây để data không mất khi Space restart
RUN mkdir -p /data
ENV DATABASE_URL="sqlite:////data/locket.db"

# HF Spaces bắt buộc lắng nghe 0.0.0.0:7860
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
