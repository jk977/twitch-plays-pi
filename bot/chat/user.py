# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/user.py
# Compiled at: 2017-10-13 15:24:02
# Size of source mod 2**32: 658 bytes
import config
import json
from interfaces.serializable import Serializable

class User(Serializable):

    def __init__(self, name):
        self._name = name

    def __eq__(self, other):
        return isinstance(other, User) and self.name == other.name

    def __hash__(self):
        return hash(self._name)

    @property
    def admin(self):
        return self._name == config.owner

    @property
    def name(self):
        return self._name

    def serialize(self):
        fields = {'name': self._name}
        return json.dumps(fields)

    def deserialize(serialized):
        fields = json.loads(serialized)
        return User(**fields)