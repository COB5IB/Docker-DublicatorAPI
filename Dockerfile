FROM python:3.10-slim
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

WORKDIR /app
#COPY crt-converted/*.crt /usr/local/share/ca-certificates/
#RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates
COPY duplicator.py .
RUN pip install flask requests
EXPOSE 6000
CMD ["python", "duplicator.py"]
