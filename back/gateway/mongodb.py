import re
from flask import Flask
from flask_pymongo import PyMongo


class RedundantException(Exception):
    pass


class MongoDB(object):
    YT_LINK_RE = re.compile(r"https:\/\/www\.youtube\.com\/watch\?v=(\S+)")

    def __init__(self, app: Flask, uri: str) -> None:
        self._mongo = PyMongo(app, uri)
        self._mongo_users = self._mongo.cx.get_database("users_db")["users"]

    def insert_user(self, email: str, target_url: str):
        """Assign given youtube vide url to the user"""
        video_id = self._fetch_video_url(target_url)

        if not list(self._mongo_users.find({"email": email})):
            self._mongo_users.insert_one({"email": email})

        if list(self._mongo_users.find({"email": email, "videos": video_id})):
            raise RedundantException("You already queued the video")

        self._mongo_users.update_one({"email": email}, {"$push": {"videos": video_id}})

    def _fetch_video_url(self, url: str) -> str:
        res = self.YT_LINK_RE.match(url)
        if not res:
            raise RuntimeError("Can't parse YouTube vide URL")
        return res.group(1)
