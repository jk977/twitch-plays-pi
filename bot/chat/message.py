# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/message.py
# Compiled at: 2017-10-13 01:12:00
# Size of source mod 2**32: 1475 bytes
import json
import time
from chat.user import User
from interfaces.serializable import Serializable

class Message(Serializable):

    def __init__(self, author, content, time=time.time()):
        if isinstance(author, str):
            author = User(author)
        elif not isinstance(author, User):
            raise ValueError('Author must be a string or User object.')
        self._author = author
        self._content = content
        self._time = time

    def __eq__(self, other):
        return isinstance(other, Message) and self.author == other.author and self.content == other.content and self.timestamp == other.timestamp

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._content

    @property
    def timestamp(self):
        return self._time

    def serialize(self):
        fields = {'author': self._author.serialize(),
         'content': self._content,
         'time': self._time}
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