class Chatter(object):
    def __init__(self, button='', roles=[]):
        self._button = button
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
    def role(self):
        return self._roles

    def add_role(self, role):
        self._roles.append(role)

    def clear_roles(self):
        self._roles = []
