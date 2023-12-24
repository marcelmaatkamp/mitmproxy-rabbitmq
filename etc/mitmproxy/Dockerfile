ARG MITMPROXY_VERSION
FROM mitmproxy/mitmproxy:${MITMPROXY_VERSION}

COPY requirements.txt requirements.txt
RUN \
    pip install -r requirements.txt