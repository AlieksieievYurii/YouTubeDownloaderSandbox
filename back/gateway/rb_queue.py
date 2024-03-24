"""Contains Queue that wraps Pika and allowing to automatically reconnect
due to closing connection by heartbeats"""

import json
import pika


class Queue(object):
    """Adapter for Pika connection that allows to automatically reconnect"""

    def __init__(self, host: str, username: str, password: str):
        self._params = pika.ConnectionParameters(
            host,
            credentials=pika.PlainCredentials(
                username,
                password,
            ),
        )
        self._connection = None
        self._channel = None

    def publish_job(self, youtube_url: str, video_id: str) -> None:
        """
        Publishes job(message containing info of
        what to download from YouTube) into the queue
        """
        key = "jobs"
        body = {"url": youtube_url, "video_id": video_id}

        try:
            self._publish(key, body)
        except pika.exceptions.StreamLostError:
            self._connect()
            self._publish(key, body)

    def _publish(self, key: str, body: dict) -> None:
        if not self._connection:
            self._connect()

        self._channel.basic_publish(
            exchange="",
            routing_key=key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    def _connect(self) -> None:
        self._connection = pika.BlockingConnection(self._params)
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue="jobs")
