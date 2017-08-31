import re
from votes.option import Option

class VoteManager:
    def __init__(self, options=None, threshold=1):
        self._options = [] if options is None else list(set(options))
        self._threshold = threshold

    def __find_option(self, name):
        if name is None:
            raise TypeError('Option name must be a string.')

        for option in self._options:
            if option.name == name:
                return option

        raise ValueError('Option not in list.')

    @property
    def threshold(self):
        return self._threshold

    def vote_total(self):
        total = 0
        for option in self._options:
            total += option.vote_count()
        return total

    def add_vote(self, user, option_name):
        """Returns vote count for option after voting"""
        # removes old vote
        try:
            user.unvote(self)
        except TypeError:
            pass

        # adds new vote
        try:
            option = self.__find_option(option_name)
            option.add_voter(user)
            votes = option.vote_count()
        except ValueError:
            option = Option(name=option_name, voters=[user])
            self._options.append(option)
            votes = 1

        return votes

    def remove_vote(self, user):
        """Returns vote count for option after removing vote"""
        try:
            option = self.__find_option(user.choice)
            option.remove_voter(user)
            votes = option.vote_count()

            if votes == 0:
                self._options = [opt for opt in self._options if opt.name != option.name]
        except ValueError:
            votes = 0

        return votes

    def reset(self):
        for option in self._options:
            for voter in option.voters:
                voter.unvote(self)
                option.remove_voter(voter)
