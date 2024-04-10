from dataclasses import dataclass
from unittest.mock import create_autospec

import pytest

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.domain.entity import Entity
from src.core._shared.events.event import Event


@dataclass(kw_only=True)
class DummyEntity(Entity):
    def validate(self):
        pass


@dataclass(frozen=True)
class DummyEvent(Event):
    pass


class TestDispatch:
    @pytest.fixture
    def entity(self):
        entity = DummyEntity(message_bus=create_autospec(AbstractMessageBus))
        return entity

    def test_append_event_and_dispatch_to_message_bus(self, entity):
        event = DummyEvent()
        entity.dispatch(event)

        assert entity.events == [event]
        entity.message_bus.handle.assert_called_once_with([event])
