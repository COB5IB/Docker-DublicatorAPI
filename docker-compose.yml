version: '3.8'

services:
  duplicator:
    build:
      context: ./duplicator
    environment:
      - LISTEN_PORT=5000
      - TARGET1=https://httpbin.org/post
      - TARGET2=https://postman-echo.com/post
    expose:
      - "5000"

  nginx:
    image: nginx:stable
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - duplicator
