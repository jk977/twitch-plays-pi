# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/interfaces/votemanager.py
# Compiled at: 2017-10-13 23:42:06
# Size of source mod 2**32: 784 bytes
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