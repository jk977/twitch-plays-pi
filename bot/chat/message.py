import json
import time
from interfaces.serializable import Serializable

class Message(Serializable):
    def __init__(self, author, content, time=time.time()):
        self._author = author
        self._content = content
        self._time = time

    def __eq__(self, other):
        return (isinstance(other, Message) and
                self.author == other.author and
                self.content == other.content and
                self.time == other.time)

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def time(self):
        return self._time

    def serialize(self):
        fields = {
            'author': self._author,
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

        return Message(author, content, time)