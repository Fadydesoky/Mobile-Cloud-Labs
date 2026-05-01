FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install redis pillow
CMD ["python", "app.py"]
