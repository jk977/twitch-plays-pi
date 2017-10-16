from . import *
from chat.voting.choices import Choices
from numbers import Number

class VoteManager:

    def __init__(self, threshold, on_decision=None, on_vote=None):
        '''
        Instantiates a VoteManager object.
        :param threshold: How many votes it takes to trigger on_decision
        :param on_decision: Callable function triggered when a choice's vote count exceeds threshold. Takes choice as parameter
        :param on_vote: Callable function triggered whenever a vote is cast. Takes VoteManager as parameter
        '''
        if on_decision and not callable(on_decision):
            raise TypeError('on_decision must be callable.')
        elif on_vote and not callable(on_vote):
            raise TypeError('on_vote must be callable.')

        if not isinstance(threshold, Number):
            raise TypeError('threshold must be a number.')

        self._threshold = threshold
        self._decision = on_decision
        self._vote = on_vote
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