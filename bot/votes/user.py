import copy
from votes.option import Option

class User:
    def __init__(self, name=None, choice=None, roles=None):
        self._name = name
        self._choice = choice
        self._roles = [] if roles is None else roles[:]

    @property
    def choice(self):
        return self._choice

    @property
    def name(self):
        return self._name

    @property
    def roles(self):
        return self._roles

    def add_role(self, role):
        if role not in self._roles:
            self._roles.append(role)

    def remove_role(self, role):
        self._roles = [r for r in self._roles if r != role]

    def clear_roles(self):
        self._roles = []

    def vote(self, manager, choice_name):
        vote_count = manager.add_vote(self, choice_name)
        self._choice = choice_name
        return vote_count

    def unvote(self, manager):
        vote_count = manager.remove_vote(self)
        self._choice = None
        return vote_count
