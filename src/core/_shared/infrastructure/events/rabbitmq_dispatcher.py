import json

import pika

from src.core._shared.events.event import Event
from src.core._shared.events.event_dispatcher import EventDispatcher


class RabbitMQDispatcher(EventDispatcher):
    def __init__(self, host='localhost', queue='videos.new'):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def dispatch(self, event: Event) -> None:
        if not self.connection:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(event.payload))
        print(f"Sent: {event} to queue {self.queue}")

    def close(self):
        self.connection.close()
