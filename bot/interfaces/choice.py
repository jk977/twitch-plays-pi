# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/interfaces/choice.py
# Compiled at: 2017-10-14 15:27:01
# Size of source mod 2**32: 2039 bytes
import json
from . import *
from chat.user import User
from interfaces.serializable import Serializable

class Choice(Serializable):

    def __eq__(self, other):
        return isinstance(other, Choice) and self._voters == other._voters and self.name == other.name

    def __hash__(self):
        return hash((frozenset(self._voters), self.name))

    @abstractproperty
    def name(self):
        """
        Returns name of input.
        """
        pass

    @property
    def voters(self):
        """
        Returns list of Users voting for choice.
        """
        return self._voters

    @property
    def votes(self):
        """
        Returns total vote count for choice.
        """
        return len(self._voters)

    def add_vote(self, voter):
        """
        Adds voter to list, and returns True if successful.
        :param voter: User voting for choice.
        """
        if not isinstance(voter, User):
            raise TypeError('Voter must be a User.')
        else:
            if voter in self._voters:
                return False
            self._voters.add(voter)
        return True

    def remove_vote(self, voter):
        """
        Removes voter to list, and returns True if successful.
        :param voter: User removing vote for choice.
        """
        if not isinstance(voter, User):
            raise TypeError('Voter must be a User.')
        else:
            if voter not in self._voters:
                return False
            self._voters.remove(voter)
        return True

    def clear(self):
        """
        Clears list of voters.
        """
        self._voters = set()

    def serialize(self):
        fields = {'name': self.name,
         'voters': [u.serialize() for u in self._voters]}
        return json.dumps(fields)

    @classmethod
    def deserialize(cls, serialized):
        fields = json.loads(serialized)
        name = fields['name']
        voters = [User.deserialize(u) for u in fields['voters']]
        return cls(name, voters)