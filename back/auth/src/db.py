"""Contains an interface to MySQL database"""

from flask import Flask
from flask_mysqldb import MySQL


class AuthDB(object):
    """Interface to the MySQL auth"""

    def __init__(self, app: Flask) -> None:
        self._db = MySQL(app)

    def get_user(self, email: str):
        """Returns a user of given email if exists, otherwise None"""
        cur = self._db.connection.cursor()

        res = cur.execute(
            "SELECT email, password FROM user WHERE email=%s",
            (email,),
        )

        if res > 0:
            user_row = cur.fetchone()
            return user_row[0], user_row[1]

        return None
