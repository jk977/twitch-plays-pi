import datetime
import json
import time

from chat.user import User
from interfaces.serializable import Serializable


class Message(Serializable):
    def __init__(self, author, content, timestamp=None):
        if isinstance(author, str):
            author = User(author)
        elif not isinstance(author, User):
            raise ValueError('Author must be a string or User object.')
        
        if not timestamp:
            timestamp = time.time()

        self._author = author
        self._content = content
        self._time = timestamp

    def __eq__(self, other):
        return (isinstance(other, Message) and
                self.author == other.author and
                self.content == other.content and
                self.timestamp == other.timestamp)

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def date(self):
        return datetime.datetime.fromtimestamp(self._time)

    @property
    def timestamp(self):
        return self._time

    def serialize(self):
        fields = {
            'author': self._author.serialize(),
            'content': self._content,
            'time': self._time
        }

        return json.dumps(fields)

    def deserialize(message):
        fields = json.loads(message)
        author = fields.get('author', None)
        content = fields.get('content', None)
        time = fields.get('time', None)

        if not (author and content and time):
            raise ValueError('Invalid JSON.')

        author = User.deserialize(author)
        return Message(author, content, time)