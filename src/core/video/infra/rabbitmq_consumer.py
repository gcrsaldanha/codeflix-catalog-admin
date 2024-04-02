import json
import logging
from uuid import UUID

import pika

from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia
from src.core.video.domain.value_objects import MediaStatus, MediaType
from src.django_project.video_app.repository import DjangoORMVideoRepository


logger = logging.getLogger(__name__)


# TODO: criar uma abstração/interface desse consumer/handler
class VideoConvertedRabbitMQConsumer:
    # Equivalente a uma View em Django (handler)
    def __init__(self, host='localhost', queue='videos.converted'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.queue = queue
        self.channel.queue_declare(queue=self.queue)

    def on_message(self, ch, method, properties, body):
        print(f"Received message: {body}")
        try:
            # Body payload
            payload = json.loads(body)

            # Tratamento de erro
            error_message = payload["error"]
            if error_message:
                aggregate_id_raw, _ = payload["message"]["resource_id"].split(".")
                logger.error(f"Error processing video {aggregate_id_raw}: {error_message}")
                return

            # Serialização do evento
            aggregate_id_raw, media_type_raw = payload["video"]["resource_id"].split(".")
            aggregate_id = UUID(aggregate_id_raw)
            media_type = MediaType(media_type_raw)
            encoded_location = payload["video"]["encoded_video_folder"]
            status = MediaStatus(payload["status"])

            # Execução do caso de uso
            process_audio_video_media_input = ProcessAudioVideoMedia.Input(
                video_id=aggregate_id,
                encoded_location=encoded_location,
                media_type=media_type,
                status=status,
            )
            use_case = ProcessAudioVideoMedia(video_repository=DjangoORMVideoRepository())
            use_case.execute(request=process_audio_video_media_input)
        except Exception as e:
            logger.error(f"Error processing payload {body}", exc_info=True)
            return

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_message, auto_ack=True)
        print('Consumer started. Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


if __name__ == '__main__':
    consumer = VideoConvertedRabbitMQConsumer()
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        consumer.close()
        print('Consumer stopped.')
