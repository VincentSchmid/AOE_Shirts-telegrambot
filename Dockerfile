FROM python:3.8-slim
ENV PYTHONUNBUFFERED True \
    SHIRT_POROCESSING_ADDRESS \
    TOKEN \
    CONFIG_FILE
WORKDIR /app
COPY *.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt
COPY . ./

CMD exec gunicorn --bind :$PORT --worker-class uvicorn.workers.UvicornWorker --timeout 0 main:app
