from typing import TypeVar

from src.core._shared.application.handlers import Handler
from src.core._shared.domain.events.event import Event
from src.core._shared.domain.events.event_dispatcher import EventDispatcher
from src.core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher
from src.core.video.domain.events.events import AudioVideoMediaUpdated



class PublishAudioVideoMediaUpdatedHandler(Handler):
    def __init__(self, dispatcher: EventDispatcher = None):
        self.dispatcher = dispatcher or RabbitMQDispatcher()

    def handle(self, event: AudioVideoMediaUpdated) -> None:
        print(f"Handling event {event}")
        self.dispatcher.dispatch(event)


class DummyHandler(Handler):
    def handle(self, event: Event) -> None:
        print(f"Handling event {event} with dummy handler")
