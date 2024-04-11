import json
import pika

QUEUE = "videos.converted"
HOST = "localhost"
PORT = 5672

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=HOST,
        port=PORT,
    ),
)
channel = connection.channel()
channel.queue_declare(queue=QUEUE)

message = {
    "error": "",
    "video": {
        "resource_id": "c97093dd-9685-4555-974f-9b368559c1ad.VIDEO",
        "encoded_video_folder": "/path/to/encoded/video",
    },
    "status": "COMPLETED",
}
channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(message))

print("Sent message")
connection.close()
