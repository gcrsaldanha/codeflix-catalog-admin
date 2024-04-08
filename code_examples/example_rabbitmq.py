from dataclasses import dataclass

from src.core._shared.events.event import Event
from src.core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher


@dataclass(frozen=True, kw_only=True)
class TestEvent(Event):
    data: str


dispatcher = RabbitMQDispatcher()

test_event = TestEvent(data="Test data")
dispatcher.dispatch(test_event)
