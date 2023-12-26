"""

"""
import base64
import json
import logging as log

import pika
from mitmproxy import http
from mitmproxy.http import HTTPFlow
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.channel import Channel
from pika.exchange_type import ExchangeType


class SendToRabbitMQ:
    """
            SendToRabbitMQ

        """

    connection: BlockingConnection
    channel: BlockingChannel

    def __init__(self):
        self.setup_logging()
        self.setup_rabbitmq()

    @staticmethod
    def setup_logging():
        log.basicConfig(level=log.DEBUG)

    def setup_rabbitmq(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
        self.channel = self.connection.channel()

        # exchanges
        self.channel.exchange_declare(
            exchange='request',
            exchange_type=ExchangeType.topic)
        self.channel.exchange_declare(
            exchange='response',
            exchange_type=ExchangeType.topic)

        # queues
        queue_requests = self.channel.queue_declare('requests', exclusive=False).method.queue
        queue_responses = self.channel.queue_declare('responses', exclusive=False).method.queue

        # bindings
        self.channel.queue_bind(exchange='request', queue=queue_requests, routing_key='#')
        self.channel.queue_bind(exchange='response', queue=queue_responses, routing_key='#')

    def response(self, flow: http.HTTPFlow) -> None:
        self.publish_flow_to_rabbitmq(flow)

    def flow_as_json(self, flow: http.HTTPFlow) -> dict:
        """
             {'data': RequestData(
                http_version=b'HTTP/1.1',
                headers=Headers[(b'Host', b'mitm.it'), (b'User-Agent', b'curl/8.5.0'), (b'Accept', b'*/*'), (b'Proxy-Connection', b'Keep-Alive')],
                content=b'',
                trailers=None,
                timestamp_start=1703414232.8881466,
                timestamp_end=1703414232.8911798,
                host='mitm.it',
                port=80,
                method=b'GET',
                scheme=b'http',
                authority=b'',
                path=b'/cert/pem')}

            :param flow:
            :return:
            """
        flow_as_json: dict = {
            "request": self.flow_request_as_json(flow.request),
            "response": self.flow_response_as_json(flow.response)
        }
        return flow_as_json

    @staticmethod
    def flow_request_as_json(request: http.Request) -> dict:
        flow_request_as_json: dict = {
            "host": request.host,
            "port": request.port,
            "method": request.method,
            "scheme": request.scheme,
            "authority": request.authority,
            "path": request.path,
            "http_version": request.http_version,
            # "headers": request.headers,
            "content": base64.b64encode(request.content),
            "trailers": request.trailers,
            "timestamp_start": request.timestamp_start,
            "timestamp_end": request.timestamp_end
        }
        return flow_request_as_json

    @staticmethod
    def flow_response_as_json(response: http.Response):
        flow_response_as_json: dict = {
            "http_version": response.http_version,
            "status_code": response.status_code,
            "reason": response.reason,
            # "headers": response.headers,
            "content": base64.b64encode(response.content),
            "trailers": response.trailers,
            "timestamp_start": response.timestamp_start,
            "timestamp_end": response.timestamp_end
        }
        return flow_response_as_json

    def publish_flow_to_rabbitmq(self, flow: HTTPFlow):
        self.channel.basic_publish(
            'response',
            flow.request.host,
            str(self.flow_as_json(flow)),
            pika.BasicProperties(
                content_type='application/json',
                type='example'))


addons = [
    SendToRabbitMQ()
]
