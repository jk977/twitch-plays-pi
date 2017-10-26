import json

from . import *
from chat.user import User
from interfaces.serializable import Serializable


class Choice(Serializable):
    '''
    Represents a voting choice with a list of voters.
    '''
    def __eq__(self, other):
        return isinstance(other, Choice) and self.voters == other.voters and self.name == other.name

    def __hash__(self):
        return hash((tuple(self.voters), self.name))

    @abstractproperty
    def name(self):
        '''
        Returns name of input.
        '''
        pass

    @abstractproperty
    def voters(self):
        '''
        Returns list of users voting for choice.
        Must return an iterable with add(), remove(), and clear() implemented.
        '''
        pass

    @property
    def votes(self):
        '''
        Returns total vote count for choice.
        '''
        return len(self.voters)

    def add_vote(self, voter):
        '''
        Adds voter to list, and returns True if successful.
        :param voter: User voting for choice.
        '''
        if not isinstance(voter, User):
            raise TypeError('Voter must be a User.')
        elif voter in self.voters:
            return False

        self.voters.add(voter)
        return True

    def remove_vote(self, voter):
        '''
        Removes voter to list, and returns True if successful.
        :param voter: User removing vote for choice.
        '''
        if not isinstance(voter, User):
            raise TypeError('Voter must be a User.')
        elif voter not in self.voters:
            return False

        self.voters.remove(voter)
        return True

    def clear(self):
        self.voters.clear()

    def serialize(self):
        fields = {
            'name': self.name,
            'voters': [u.serialize() for u in self.voters]
        }

        return json.dumps(fields)

    @classmethod
    def deserialize(cls, serialized):
        fields = json.loads(serialized)
        name = fields['name']
        voters = (User.deserialize(u) for u in fields['voters'])
        return cls(name, voters)