ARG MITMPROXY_VERSION
FROM mitmproxy/mitmproxy:${MITMPROXY_VERSION}

COPY requirements.txt requirements.txt

RUN \
    apt update && \
    apt install -fy  \
      curl && \
    apt clean && \
    pip install -r requirements.txt
