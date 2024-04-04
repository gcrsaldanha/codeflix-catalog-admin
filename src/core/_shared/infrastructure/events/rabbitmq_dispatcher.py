import json

import pika

from src.core._shared.domain.events.event import Event
from src.core._shared.domain.events.event_dispatcher import EventDispatcher


class RabbitMQDispatcher(EventDispatcher):
    def __init__(self, host='localhost', queue='videos.new'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.queue = queue
        self.channel.queue_declare(queue=self.queue)

    def dispatch(self, event: Event) -> None:
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=self.serialize(event))
        print(f"Sent: {event}")

    def serialize(self, event: Event) -> bytes:
        return json.dumps(event.serialize()).encode()

    def close(self):
        self.connection.close()
