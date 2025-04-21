FROM python:3.11-slim
WORKDIR /var/task
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "run:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
