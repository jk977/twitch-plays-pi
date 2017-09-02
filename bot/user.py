from roles import Roles
from votes.option import Option


class User:
    def __init__(self, name=None, choice=None, moderator=False, owner=False):
        role = Roles.DEFAULT

        if owner:
            role |= Roles.OWNER
        elif moderator:
            role |= Roles.MOD

        self._name = name
        self._choice = choice
        self._role = role

    @property
    def choice(self):
        return self._choice

    @property
    def name(self):
        return self._name

    @property
    def is_banned(self):
        return bool(self._role & Roles.BANNED)

    @property
    def is_moderator(self):
        return bool(self._role & Roles.MOD)

    @property
    def is_owner(self):
        return bool(self._role & Roles.OWNER)

    def mod(self):
        self._role |= Roles.MOD

    def unmod(self):
        self._role &= ~Roles.MOD

    def ban(self):
        if self.is_owner:
            raise PermissionError('Can\'t ban the owner!')

        self._role |= Roles.BANNED

    def unban(self):
        self._role &= ~Roles.BANNED

    def vote(self, manager, choice_name):
        if self.is_banned:
            raise PermissionError('Banned users can\'t vote.')

        vote_count = manager.add_vote(self, choice_name)
        self._choice = choice_name
        return vote_count

    def unvote(self, manager):
        vote_count = manager.remove_vote(self)
        self._choice = None
        return vote_count
