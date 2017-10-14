from . import *
from chat.voting.choices import Choices
from numbers import Number

class VoteManager:
    def __init__(self, threshold, on_decision=lambda name: print(name)):
        if not callable(on_decision):
            raise TypeError('on_decision must be callable.')

        if not isinstance(threshold, Number):
            raise TypeError('threshold must be a number.')

        self._threshold = threshold
        self._decision = on_decision
        self._choices = Choices()

    @abstractmethod
    def cast_vote(self, user, choice_name):
        pass

    @abstractmethod
    def remove_vote(self, user, choice_name):
        pass

    @property
    def options(self):
        return self._choices

    @property
    def threshold(self):
        return self._threshold