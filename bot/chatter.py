class Chatter(object):
    def __init__(self, button='', cheat='', roles=[]):
        self._button = button
        self._cheat = cheat
        self._roles = roles

    @property
    def button(self):
        return self._button

    @button.setter
    def button(self, button):
        self._button = button

    def clear_button(self):
        self._button = ''

    @property
    def cheat(self):
        return self._cheat

    @cheat.setter
    def cheat(self, cheat):
        self._cheat = cheat

    def clear_cheat(self):
        self._cheat = ''

    @property
    def role(self):
        return self._roles

    def add_role(self, role):
        self._roles.append(role)

    def clear_roles(self):
        self._roles = []
