# codeflix-catalog-admin
Administração de Catálogo – Codeflix - Python


## Git Branch para cada módulo
- [Módulo 2: Entidade Category](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-2-category)
- [Módulo 3: Casos de uso Category](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-3-category-use-cases)
- [Módulo 4: casos de uso Category - pt 2](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-4-category-use-cases-part-2)
- [Módulo 5: Implementando nossa API](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-5-django-api)
- [Módulo 6: Implementando nossa API - pt 2](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-6-django-api-parte-2)
- [Módulo 7: Domain Genre](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-7-genre-domain)
- [Módulo 8: API Genre](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-8-genre-api)
- [Módulo 9: API CastMember](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-9-cast-member)
    - [Desafio: Implementar Domain e API CastMember](https://github.com/gcrsaldanha/codeflix-catalog-admin/blob/main/referencias/Desafio%3A%20API%20CastMember.md)
- [Módulo 10: Refatoração](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-10-refatoracao)
    - [Desafio: Paginação e Refatoração](https://github.com/gcrsaldanha/codeflix-catalog-admin/blob/main/referencias/Desafio%3A%20Pagina%C3%A7%C3%A3o%20e%20Refatora%C3%A7%C3%A3o.md)
- [Módulo 11: Domain Video](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-11-domain-video-completo)
  - [Pull Request](https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/9)
  - [Desafio: Implementar API Video](https://github.com/gcrsaldanha/codeflix-catalog-admin/blob/main/referencias/Desafio%3A%20API%20para%20cria%C3%A7%C3%A3o%20de%20v%C3%ADdeo%20sem%20m%C3%ADdia.md)
- [Módulo 12: Upload de Vídeo](https://github.com/gcrsaldanha/codeflix-catalog-admin/tree/modulo-12-upload-de-video)
  - [Pull Request](https://github.com/gcrsaldanha/codeflix-catalog-admin/pull/11)



# Notes domain events

- PublishVideoMediaReplacedInQueueHandler -> video/applications
  - Depends on MessageBroker
    - broker.publish('video_media_replaced_in_queue', video.id)
- UseCase:
  - Depends on EventPublisher
  - events = video.flush_events()
    self.event_publisher.publish(events)
- Luiz fez emissão de eventos "interna", ao próprio aggregate
- Application layer: responsável por dispatch events to aggregate para o mundo exterior


- Application Layer
  - Sem eventos: application layer logo após "update_video_media" -> envia requisição para o encoder
  - UoW
    - gathers events raised by Domain Model (domain events)
    - publishes events to Message Bus
  - Message Bus
    - dispatches events to handlers
    - https://www.cosmicpython.com/book/chapter_08_events_and_message_bus.html#_the_message_bus_maps_events_to_handlers
    - Service Layer: Message Bus - 
```python
def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)

def send_out_of_stock_notification(event: events.OutOfStock):
    email.send_mail(
        "stock@made.com",
        f"Out of stock for {event.sku}",
    )

HANDLERS = {
    events.OutOfStock: [send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
```

Option 1: service calls messagebus.handle(aggregate.events)
- better than calling the encoder directly

```python
import src.core._shared.application.abstract_message_bus

HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.BatchQuantityChanged: [handlers.change_batch_quantity],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}


class AbstractMessageBus:
    HANDLERS: Dict[Type[events.Event], List[Callable]]

    def handle(self, event: events.Event):
        for handler in self.HANDLERS[type(event)]:
            handler(event)


class MessageBus(AbstractMessageBus):
    HANDLERS = {
        events.OutOfStock: [send_out_of_stock_notification],

    }


class FakeMessageBus(src.core._shared.application.abstract_message_bus.AbstractMessageBus):
    def __init__(self):
        self.events_published = []  # type: List[events.Event]
        self.HANDLERS = {
            events.OutOfStock: [lambda e: self.events_published.append(e)]
        }
```


My aggregate method update_video adds an event to itself
The application layer, will poll these events and dispatch them to the message bus via message_bus.dispatch(event)
the message bus has a dict of event type and list of callable (handler).
the `dispatch` method will call the proper handler.
one of the handlers in handlers.py (in the application layer) is the publish_video_updated_event(ev: AudioVideoMediaUpdatedEvent)
This handler, in turn, will call the RabbitMQPublisher publish method passing the event.
This publisher should be a thin layer around RabbitMQ that will in fact publish the event payload to the `videos.new` queue.


+----------------+       +------------------+       +---------------+       +-------------------+       +------------------+       +----------------------+
| VideoAggregate +<------+ ApplicationLayer +------>+ MessageBus    +------>+ handlers.py       +------>+ RabbitMQPublisher+------>+ RabbitMQ (videos.new)|
+-------+--------+       +---------+--------+       +-------+-------+       +-------------------+       +------------------+       +----------------------+
        |                          |                        |                                                        |
        | update_video             | aggregate.events       | dispatch(event)                                        | publish(event)
        |------------------------->|----------------------->|------------------------------------------------------->|
