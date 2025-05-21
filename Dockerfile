FROM python:3.12-slim AS builder
WORKDIR /app

# otimizações de imagem
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
 && apt-get install -y build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 5000
CMD ["gunicorn", "--chdir", "/app", "main:create_app()", "--bind", "0.0.0.0:5000", "--workers", "4", "--log-level", "info"]
