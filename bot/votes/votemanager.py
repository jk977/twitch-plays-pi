import numbers
from votes.option import Option


class VoteManager:
    def __init__(self, options=None, threshold=1, on_decision=None):
        """
        Initializes vote manager with specified threshold (may be callable or a number)
        :param threshold: Number or function that returns number.
        :param predicate: Function that takes a string and returns boolean value
        :param on_decision: Callable function that takes option name as argument and is executed when threshold is exceeded.
        """
        if not callable(on_decision):
            raise TypeError('"on_decision" must be callable')

        if callable(threshold) and not isinstance(threshold(), numbers.Number):
            raise TypeError('"threshold" must be a number or a function that returns a number')

        self._options = [] if options is None else list(set(options))
        self._threshold = threshold
        self._on_decision = on_decision


    def __find_option(self, name):
        if name is None:
            raise TypeError('Option name must be a string.')

        for option in self._options:
            if option.name == name:
                return option

        raise ValueError('Option not in list.')


    @property
    def threshold(self):
        if callable(self._threshold):
            return self._threshold()
        else:
            return self._threshold


    def vote_total(self):
        total = 0
        for option in self._options:
            total += option.vote_count()
        return total


    def add_vote(self, user, option_name):
        try:
            user.unvote(self)
        except TypeError:
            # user hasn't voted
            pass

        try:
            # adds vote to option if already exists
            option = self.__find_option(option_name)
            option.add_voter(user)
            votes = option.vote_count
        except ValueError:
            # adds new option to list
            option = Option(name=option_name, voters=[user])
            self._options.append(option)
            votes = 1

        if votes >= self.threshold:
            self._on_decision(option_name)
            self.reset


    def remove_vote(self, user):
        try:
            option = self.__find_option(user.choice)
            option.remove_voter(user)
            votes = option.vote_count()

            # removes option from list if no votes
            if votes == 0:
                self._options = [opt for opt in self._options if opt.name != option.name]
        except TypeError:
            pass


    def reset(self):
        """Resets vote data."""
        for option in self._options:
            for voter in option.voters:
                voter.unvote(self)
                option.remove_voter(voter)
