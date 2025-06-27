# Build-time proxy desteği
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

FROM python:3.11-slim

# Proxy ayarları ENV olarak geçilsin (opsiyonel)
ENV HTTP_PROXY=$HTTP_PROXY \
    HTTPS_PROXY=$HTTPS_PROXY \
    NO_PROXY=$NO_PROXY

RUN pip install --no-cache-dir flask requests

WORKDIR /app

COPY duplicator.py .

RUN mkdir -p /logs

ENV LOG_DIR=/logs \
    LISTEN_PORT=6000 \
    FORWARD_TIMEOUT=5

CMD ["python", "duplicator.py"]
