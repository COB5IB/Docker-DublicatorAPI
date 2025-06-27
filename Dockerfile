FROM python:3.11-slim

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

WORKDIR /app

COPY duplicator.py .

RUN pip install --no-cache-dir flask requests

ENV LOG_DIR=/logs \
    LISTEN_PORT=6000 \
    FORWARD_TIMEOUT=5

CMD ["python", "duplicator.py"]
