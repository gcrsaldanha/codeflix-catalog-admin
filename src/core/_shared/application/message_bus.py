import logging
from typing import Type, TypeVar, List

from src.core._shared.application.handlers import Handler
from src.core._shared.domain.events.event import Event, TEvent
from src.core.video.application.handlers import PublishAudioVideoMediaUpdatedHandler, DummyHandler
from src.core.video.domain.events.events import AudioVideoMediaUpdated

logger = logging.getLogger(__name__)

class MessageBus:
    EVENT_HANDLERS: dict[Type[TEvent], List[Handler[TEvent]]] = {
        AudioVideoMediaUpdated: [PublishAudioVideoMediaUpdatedHandler(), DummyHandler()]
    }

    def dispatch(self, events: list[Event]) -> None:
        for event in events:
            for handler in MessageBus.EVENT_HANDLERS[type(event)]:
                try:
                    print(f"handling event {event} with handler {handler}")
                    handler.handle(event)
                except Exception:
                    logger.exception("Exception handling event %s", event)
                    continue

    # TODO: register(event: Type[TEvent], handler: Handler[TEvent]) -> None:
