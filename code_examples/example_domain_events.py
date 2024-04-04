class VideoRepository:
    def __init__(self):
        self.storage = {}

    def find_by_id(self, video_id):
        return self.storage.get(video_id)

    def save(self, video):
        self.storage[video.id] = video


class AudioVideoMediaReplacedHandler:
    def __init__(self, broker):
        self.broker = broker

    def handle(self, event):
        # Convert domain event to message
        message = {'video_id': event.video_id, 'new_media_url': event.new_media_url}
        # Send message to RabbitMQ
        self.broker.publish('videos.new', message)


class DomainEventPublisher:  # This can live in Aggregate
    def __init__(self):
        self.subscribers = []

    def subscribe(self, event_type, handler):
        self.subscribers.append((event_type, handler))

    def publish(self, events):
        for event in events:
            for event_type, handler in self.subscribers:
                if isinstance(event, event_type):
                    handler.handle(event)


class UploadVideo:
    def __init__(self, video_repository, event_publisher):
        self.video_repository = video_repository
        self.event_publisher = event_publisher

    def upload_video(self, video_id, video_data, new_media_url):
        video = self.video_repository.find_by_id(video_id) or VideoAggregate()
        video.update_video(video_id, new_media_url)
        self.video_repository.save(video)
        events = video.flush_events()
        self.event_publisher.publish(events)


if __name__ == '__main__':
    from domain.aggregates.video_aggregate import VideoAggregate
    from infrastructure.messaging.rabbitmq_broker import RabbitMQBroker
    from infrastructure.event_publisher import DomainEventPublisher
    from infrastructure.repositories.video_repository import VideoRepository
    from application.upload_video import UploadVideo
    from application.event_handlers.audio_video_media_replaced_handler import AudioVideoMediaReplacedHandler
    from domain.events.audio_video_media_replaced import AudioVideoMediaReplaced

    # Instantiate infrastructure components
    rabbitmq_broker = RabbitMQBroker(host='localhost', queue='videos.new')
    event_publisher = DomainEventPublisher()

    # Instantiate repository
    video_repository = VideoRepository()

    # Subscribe event handlers to the publisher
    audio_video_media_replaced_handler = AudioVideoMediaReplacedHandler(rabbitmq_broker)
    event_publisher.subscribe(AudioVideoMediaReplaced, audio_video_media_replaced_handler)

    # Instantiate the use case service
    upload_video_service = UploadVideoService(video_repository, event_publisher)

    # Example usage
    video_id = "123"
    video_data = {}  # Assuming some video data
    new_media_url = "http://example.com/newvideo.mp4"
    upload_video_service.upload_video(video_id, video_data, new_media_url)
