import numbers

from emulator import Emulator
from votes.option import Option


class VoteManager:
    _vote_file = '../game/votes.txt'


    def __init__(self, options=None, threshold=1, on_decision=None, debug=False):
        """
        Initializes vote manager with specified threshold (may be callable or a number)
        :param threshold: Number or function that returns number.
        :param predicate: Function that takes a string and returns boolean value
        :param on_decision: Callable function that takes option name as argument and is executed when threshold is exceeded.
        :param debug: If set to true, prevents sending to stream overlay.
        """
        if not callable(on_decision):
            raise TypeError('"on_decision" must be callable')

        if callable(threshold) and not isinstance(threshold(), numbers.Number):
            raise TypeError('"threshold" must be a number or a function that returns a number')

        self._options = [] if options is None else list(set(options))
        self._threshold = threshold
        self._on_decision = on_decision
        self._debug = debug


    def __find_option(self, name):
        if not name:
            raise TypeError('Option name must be a string.')

        for option in self._options:
            if option.name == name:
                return option

        raise ValueError('Option not in list.')


    def __export_top(self, count):
        if self.threshold == 1:
            return

        # gets all options with a nonzero number of votes, sorted by vote count
        opts = [o for o in sorted(self._options, key=lambda o: o.vote_count) if o.vote_count > 0]
        top = ['{}: {}'.format(Emulator.parse_input(o.name), o.vote_count) for o in opts[:count]]

        with open(VoteManager._vote_file, 'w') as file:
            for opt in top:
                file.write(opt + '\n')


    @property
    def threshold(self):
        if callable(self._threshold):
            return self._threshold()
        else:
            return self._threshold


    @property
    def vote_total(self):
        total = 0
        for option in self._options:
            total += option.vote_count
        return total


    def add_vote(self, user, option_name):
        if user.is_banned:
            return

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

        if not self._debug:
            self.__export_top(3)

        if votes >= self.threshold:
            self._on_decision(option_name)
            self.reset()


    def remove_vote(self, user):
        try:
            option = self.__find_option(user.choice)
            option.remove_voter(user)
            votes = option.vote_count

            # removes option from list if no votes
            if votes == 0:
                self._options = [opt for opt in self._options if opt.name != option.name]
        except (ValueError, TypeError):
            pass


    def reset(self):
        """Resets vote data."""
        for option in self._options:
            for voter in option.voters:
                voter.unvote(self)
                option.remove_voter(voter)

        with open(VoteManager._vote_file, 'w') as file:
            pass
