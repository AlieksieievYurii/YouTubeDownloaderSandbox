"""Contains Middleware interface for working with MongoDB"""

from flask import Flask
from flask_pymongo import PyMongo


class RedundantException(Exception):
    """Supposed to be raised once user already have downloaded audio"""


class MongoDB(object):
    """Interface for working with MongoDB"""

    def __init__(self, app: Flask, uri: str) -> None:
        self._mongo = PyMongo(app, uri)
        self._mongo_users = self._mongo.cx.get_database("main")["users"]
        self._jobs = self._mongo.cx.get_database("main")["items"]
        self._mongo.cx.get_database("main")

    def insert_user(self, email: str, video_id: str):
        """Assign given youtube vide url to the user"""

        if not list(self._mongo_users.find({"email": email})):
            self._mongo_users.insert_one({"email": email})

        if list(self._mongo_users.find({"email": email, "items": video_id})):
            raise RedundantException("You already queued the video")

        self._mongo_users.update_one(
            {"email": email}, {"$push": {"items": video_id}}
        )

    def insert_job(self, target_url: str, video_id: str):
        """Registers item (job) which contains information about downloading"""
        job = self._jobs.find_one({"video_id": video_id})
        if not job:
            body = {
                "url": target_url,
                "video_id": video_id,
                "progress": 0,
                "state": "QUEUED",
            }
            self._jobs.insert_one(body)

    def remove_item_from_user(self, email: str, video_id) -> None:
        """Removes video item from given user"""
        self._mongo_users.update_one(
            {"email": email}, {"$pull": {"items": video_id}}
        )

    def get_user_items(self, email: str) -> list:
        """Returns the given user's list of downloaded audios"""
        user = self._mongo_users.find_one({"email": email})
        if not user:
            return []
        return list(
            self._jobs.find({"video_id": {"$in": user["items"]}}, {"_id": 0})
        )
