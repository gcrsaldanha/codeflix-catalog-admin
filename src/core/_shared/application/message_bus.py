import logging
from typing import Type, List

from src.core._shared.application.handlers import Handler
from src.core._shared.domain.events.event import Event, TEvent
from src.core._shared.infrastructure.events.rabbitmq_dispatcher import RabbitMQDispatcher
from src.core.video.application.events.handlers import PublishAudioVideoMediaUpdatedHandler, DummyHandler
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core.video.domain.events import AudioVideoMediaUpdated

logger = logging.getLogger(__name__)


class MessageBus:
    EVENT_HANDLERS: dict[Type[TEvent], List[Handler[TEvent]]] = {
        AudioVideoMediaUpdatedIntegrationEvent: [
            PublishAudioVideoMediaUpdatedHandler(RabbitMQDispatcher.factory_with_queue("videos.new")),
        ],
        AudioVideoMediaUpdated: [
            DummyHandler(),
        ],
    }

    def dispatch(self, events: list[Event]) -> None:
        for event in events:
            for handler in MessageBus.EVENT_HANDLERS[type(event)]:
                try:
                    handler.handle(event)
                except Exception:
                    logger.exception("Exception handling event %s", event)
                    continue
