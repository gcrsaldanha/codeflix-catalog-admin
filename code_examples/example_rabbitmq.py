from dataclasses import dataclass

from src.core._shared.domain.events.domain_event import DomainEvent
from src.core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher


@dataclass(frozen=True, kw_only=True)
class TestEvent(DomainEvent):
    data: str


dispatcher = RabbitMQDispatcher()

test_event = TestEvent(data="Test data")
dispatcher.dispatch(test_event)
