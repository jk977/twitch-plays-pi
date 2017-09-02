class Option:
    def __init__(self, name='', voters=[]):
        self._name = name
        self._voters = list(set(voters))

    @property
    def name(self):
        return self._name

    @property
    def voters(self):
        return self._voters

    def reset():
        self._voters = set()

    def add_voter(self, user):
        if user not in self._voters:
            self._voters.append(user)

    def remove_voter(self, user):
        self._voters = [voter for voter in self._voters if voter != user]

    def vote_count(self):
        return len(self._voters)