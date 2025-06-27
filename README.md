# 🔁 HTTPS Destekli API İstek Çoklayıcı (Duplicator)

Bu proje, gelen bir API `POST` isteğini iki farklı hedefe (TARGET1 ve TARGET2) çoğaltarak HTTPS üzerinden ileten bir HTTP Duplicator servisidir.  
NGINX ile reverse proxy kurularak HTTPS desteği sağlanır.

---

## 🚀 Özellikler

- Gelen veriyi `TARGET1` ve `TARGET2` adreslerine çoğaltır
- HTTPS endpoint'i ile çalışır
- Flask + Requests ile hızlı, sade ve genişletilebilir
- Log dosyası: `/logs/duplicator.log`

---

## 🏗️ Mimari

```bash
📦 Docker-DuplicatorAPI/
├── duplicator/            # Flask app
│   ├── Dockerfile
│   └── duplicator.py
├── nginx/                 # NGINX reverse proxy
│   ├── nginx.conf
│   └── ssl/
│       ├── fullchain.pem  # SSL certificate
│       └── privkey.pem    # SSL private key
└── docker-compose.yml
```

---

## ⚙️ Gereksinimler

- Docker
- Docker Compose
- (Opsiyonel) Gerçek domain ve sertifika veya self-signed sertifika

---

## ⚙️ Kurulum ve Çalıştırma

### 1. Ortam Değişkenlerini Ayarla

`docker-compose.yml` içinde hedefleri tanımla:

```yaml
environment:
  - TARGET1=https://httpbin.org/post
  - TARGET2=https://postman-echo.com/post
```

### 2. SSL Sertifikalarını Yerleştir

```bash
mkdir -p nginx/ssl
cp your_cert.pem nginx/ssl/fullchain.pem
cp your_key.pem nginx/ssl/privkey.pem
```

### 3. Uygulamayı Başlat

```bash
docker-compose up --build
```

---

## ✅ Test Et

```bash
curl -k -X POST https://localhost/ -d "merhaba burak"
```

> `-k` flag'i self-signed sertifikalar için kullanılır.

Sağlık kontrolü için:

```bash
curl -k https://localhost/healthz
```

---

## 🗂 Loglar

Tüm gelen istekler ve hedef yanıt durumları şu dosyaya yazılır:

```
/logs/duplicator.log
```

---

## 📌 Notlar

- HTTPS portu dış dünyaya açık: `443`
- İçeride Flask HTTP çalışır: `5000`
- NGINX proxy ile HTTPS terminasyonu yapılır.

---

## 📜 Lisans

MIT Lisansı
