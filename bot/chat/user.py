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