""" Downloader is a service that listens for incoming messages from the
RabbitQM. Once it receives 'job' containing YouTube video URL, it starts
downloading audio file. Once the file is downloaded, the service updates
an item in the database.
"""

import json
from pathlib import Path
import tempfile
from gridfs import GridFS
import pika
from pymongo import MongoClient
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

client = MongoClient(variables.MONGODB)

fs_videos = GridFS(client.get_database("audio_files"))

items_collection = client.get_database("main").get_collection("items")


def set_item_status_as_downloading(video_id: str) -> None:
    """Sets the item as downloading in the DB"""
    items_collection.update_one(
        {"video_id": video_id}, {"$set": {"state": "DOWNLOADING"}}
    )


def set_item_status_as_failed(video_id: str, message: str) -> None:
    """Sets the item as failed"""
    items_collection.update_one(
        {"video_id": video_id},
        {"$set": {"state": "FAILED", "error_message": message}},
    )


def set_item_status_as_downloaded(
    audio_file_id: str, video_id: str, size: int
) -> None:
    """Sets the item as downloaded in the DB"""
    items_collection.update_one(
        {"video_id": video_id},
        {
            "$set": {
                "audio_file_id": audio_file_id,
                "state": "DOWNLOADED",
                "size": size,
            }
        },
    )


def on_progress(video_id: str, downloaded: int, size: int):
    pass
    # TODO and test
    # items_collection.update_one(
    #     {"video_id": video_id}, {"$set": {"progress": downloaded}}
    # )
    # print("Prog: ", end="")
    # print(size)
    # print(f"{size} / {downloaded}")


def on_reveice_job(ch, method, properties, body) -> None:
    """Callback function that is trigger once there is a job in queue"""
    data: dict = json.loads(body)
    video_id: str = data["video_id"]
    origin_video_url = data["url"]
    file = Path(tempfile.gettempdir()) / f"{video_id}.mp3"
    print(f"Start downloading {origin_video_url}")
    set_item_status_as_downloading(video_id)
    try:
        youtube_downloader.download(
            origin_video_url, file, lambda d, s: on_progress(video_id, d, s)
        )
    except Exception as error:
        print(error)
        set_item_status_as_failed(video_id, str(set_item_status_as_failed))
    uid = fs_videos.put(file.read_bytes())
    set_item_status_as_downloaded(uid, video_id, file.stat().st_size)


def main() -> None:
    """Entrypoint function"""
    channel.basic_consume(queue="jobs", on_message_callback=on_reveice_job)
    print("Waiting for jobs...")
    channel.start_consuming()


if __name__ == "__main__":
    channel.queue_declare("jobs")
    main()
