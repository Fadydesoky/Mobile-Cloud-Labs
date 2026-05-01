# 📦 Lab 5 - Local Serverless Event-Driven Pipeline

This lab implements a local serverless-style architecture using Docker and Redis.

---

## 🧠 Architecture

Pipeline flow:

Input Image → Event Source → Redis Stream → Router → Functions → Output Image

---

## ⚙️ Technologies

- Docker & Docker Compose
- Redis Streams
- Flask (FaaS simulation)
- Pillow (image processing)

---

## 🚀 How to Run

```bash
docker compose up --build
