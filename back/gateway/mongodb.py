"""Contains Middleware interface for working with MongoDB"""

from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
import gridfs


class RedundantException(Exception):
    """Supposed to be raised once user already have downloaded audio"""


class NotReadyToDownload(Exception):
    """Supposed to be raised when item is not downloaded"""


class MongoDB(object):
    """Interface for working with MongoDB"""

    def __init__(self, app: Flask, uri: str) -> None:
        self._mongo = PyMongo(app, uri)
        self._mongo_users = self._mongo.cx.get_database("main")["users"]
        self._jobs = self._mongo.cx.get_database("main")["items"]
        self._audios = gridfs.GridFS(
            self._mongo.cx.get_database("audio_files")
        )
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

    def has_user_video(self, email: str, video_id: str) -> bool:
        """Checks if user has given video"""
        user = self._mongo_users.find_one({"email": email})
        return video_id in user["items"]

    def get_youtube_url(self, video_id: str) -> str:
        """Returns origin YouTube url for given video id"""
        result = self._jobs.find_one({"video_id": video_id})
        return result["url"]

    def set_queued_state(self, video_id: str) -> None:
        """Sets a job as queued again"""
        self._jobs.update_one(
            {"video_id": video_id},
            {
                "$set": {
                    "progress": 0,
                    "state": "QUEUED",
                    "total_size": 0,
                    "error_message": "",
                    "audio_file_id": "",
                    "downloaded_size": 0,
                }
            },
        )

    def get_audio_file(self, video_id: str):
        """
        Returns file interface containing downloaded audio of given video id
        """
        item = self._jobs.find_one(
            {"video_id": video_id, "state": "DOWNLOADED"}
        )
        if item:
            return self._audios.get(ObjectId(item["audio_file_id"]))
        raise NotReadyToDownload(
            f"Item (video_id: {video_id}) is not downloaded yet"
        )
