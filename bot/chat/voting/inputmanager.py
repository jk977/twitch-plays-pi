# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/voting/inputmanager.py
# Compiled at: 2017-10-14 00:38:28
# Size of source mod 2**32: 1119 bytes
from interfaces.votemanager import VoteManager

class InputManager(VoteManager):

    def cast_vote(self, user, choice_name):
        """
        Cast vote towards choice_name for the given user and return True if decision is reached
        (i.e., vote count for choice exceeds threshold after vote).
        :param user: User casting the vote.
        :param choice_name: Name of choice to vote for.
        """
        if choice_name not in self._choices:
            self._choices.add_choice(choice_name)
        self._choices.remove_vote(user, choice_name)
        self._choices.add_vote(user, choice_name)
        choice = self._choices.get_choice(choice_name)
        if choice.votes >= self.threshold:
            self._decision(choice)
            self._choices.clear_votes()
            return True
        return False

    def remove_vote(self, user, choice_name):
        """
        Remove vote and return True on success.
        :param user: User to remove vote for.
        :param choice_name: Name of choice to remove vote for.
        """
        return self._choices.remove_vote(user, choice_name)