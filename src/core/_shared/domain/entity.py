import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

from src.core._shared.domain.events.domain_event import DomainEvent
from src.core._shared.domain.events.event_dispatcher import EventDispatcher
from src.core._shared.domain.notification import Notification
from src.core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid.uuid4)
    notification: Notification = field(default_factory=Notification, init=False)
    events: list[DomainEvent] = field(default_factory=list, init=False)
    event_dispatcher: EventDispatcher = field(default_factory=RabbitMQDispatcher, init=True)

    def dispatch_event(self, event: DomainEvent) -> None:
        self.events.append(event)
        self.event_dispatcher.dispatch(event)

    def __eq__(self, other: "Entity") -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    @abstractmethod
    def validate(self):
        pass
