from dataclasses import dataclass
from unittest.mock import create_autospec

from src.core._shared.application.handlers import Handler
from src.core._shared.events.event import Event
from src.core._shared.events.message_bus import MessageBus


@dataclass(frozen=True)
class DummyEvent(Event):
    name: str = "dummy"


class TestMessageBus:
    def test_calls_handler_with_message(self) -> None:
        dummy_handler = create_autospec(Handler)
        message_bus = MessageBus()
        event = DummyEvent()

        message_bus.handlers[type(event)] = [dummy_handler]
        message_bus.handle([event])

        dummy_handler.handle.assert_called_once_with(event)
