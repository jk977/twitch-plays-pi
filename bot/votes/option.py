class Option:
    def __init__(self, name='', voters=[]):
        self._name = name
        self._voters = list(set(voters))

    def __lt__(self, other):
        return len(self._voters) < len(other._voters)

    def __gt__(self, other):
        return len(self._voters) > len(other._voters)

    @property
    def name(self):
        return self._name

    @property
    def voters(self):
        return self._voters

    @property
    def vote_count(self):
        return len(self._voters)

    def reset():
        self._voters = set()

    def add_voter(self, user):
        if user.name not in [v.name for v in self._voters]:
            self._voters.append(user)

    def remove_voter(self, user):
        self._voters = [voter for voter in self._voters if voter.name != user.name]
