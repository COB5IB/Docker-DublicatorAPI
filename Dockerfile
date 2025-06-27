# Build sırasında proxy ayarlarını almak için arg tanımları
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

FROM python:3.11-slim

# Proxy bilgilerini environment olarak da geçir (opsiyonel, bazı pip işlemleri için gerekebilir)
ENV HTTP_PROXY=$HTTP_PROXY \
    HTTPS_PROXY=$HTTPS_PROXY \
    NO_PROXY=$NO_PROXY

# Gerekli Python paketlerini yükle
RUN pip install --no-cache-dir flask requests

# Çalışma dizini
WORKDIR /app

# Uygulama dosyasını konteynıra kopyala
COPY duplicator.py .

# Log klasörü oluştur
RUN mkdir -p /logs

# Ortam değişkenleri
ENV LOG_DIR=/logs \
    LISTEN_PORT=6000 \
    FORWARD_TIMEOUT=5

# Uygulama başlat
CMD ["python", "duplicator.py"]
