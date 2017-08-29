class Choice():
    def __init__(self, name='', voters=[]):
        self._name = name
        self._voters = set(voters)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def voters(self):
        return self._voters

    def reset(self):
        self._voters = set()

    def count(self):
        return len(self._voters)

    def vote(self, user):
        if user not in self._voters:
            self._voters.add(user)
            
    def unvote(self, user):
        if user in self._voters:
            self._voters.remove(user)
