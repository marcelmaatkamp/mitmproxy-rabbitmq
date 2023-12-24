# mitmporoxy

## curl

```docker-compose.yml
  curl:
    image: curlimages/curl
    command: curl http://mitm.it/cert/pem
    environment:
      http_proxy: mitmproxy:8080
      https_proxy: mitmproxy:8080
```