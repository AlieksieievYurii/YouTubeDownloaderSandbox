from flask import Flask
from flask_pymongo import PyMongo


class RedundantException(Exception):
    pass


class MongoDB(object):

    def __init__(self, app: Flask, uri: str) -> None:
        self._mongo = PyMongo(app, uri)
        self._mongo_users = self._mongo.cx.get_database("main")["users"]
        self._jobs = self._mongo.cx.get_database("main")["items"]

    def insert_user(self, email: str, video_id: str):
        """Assign given youtube vide url to the user"""

        if not list(self._mongo_users.find({"email": email})):
            self._mongo_users.insert_one({"email": email})

        if list(self._mongo_users.find({"email": email, "videos": video_id})):
            raise RedundantException("You already queued the video")

        self._mongo_users.update_one(
            {"email": email}, {"$push": {"videos": video_id}}
        )

    def insert_job(self, target_url: str, video_id: str):
        job = self._jobs.find_one({"video_id": video_id})
        if not job:
            body = {
                "url": target_url,
                "video_id": video_id,
                "progress": 0,
                "state": "QUEUED",
            }
            self._jobs.insert_one(body)
