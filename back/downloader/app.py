import json
from pathlib import Path
import pika
import youtube_downloader
import variables

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        variables.RABBITMQ_HOST,
        credentials=pika.PlainCredentials(
            username=variables.RABBITMQ_SVC_USER,
            password=variables.RABBITMQ_SVC_PASSWORD,
        ),
    )
)
channel = connection.channel()


def on_progress(downloaded: int, size: int):
    print("Prog: ", end='')
    print(size)
    print(f"{size} / {downloaded}")


def on_reveice_job(ch, method, properties, body) -> None:
    data = json.loads(body)
    file = Path("output") / f"{data["video_id"]}.mp3"
    print(f"start downloading {data["url"]}")
    youtube_downloader.download(data["url"], file, on_progress)


def main() -> None:
    channel.basic_consume(
        queue=variables.QUEUE_NAME, on_message_callback=on_reveice_job
    )
    print("Waiting for jobs...")
    channel.start_consuming()


if __name__ == "__main__":
    channel.queue_declare(queue=variables.QUEUE_NAME)
    main()
