from numbers import Number
from chat.voting.choices import Choices
from nes.emuchoice import EmuChoice


class InputManager:
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

    @property
    def options(self):
        return self._choices

    @property
    def threshold(self):
        return self._threshold

    def cast_vote(self, user, choice_name):
        '''
        Cast vote towards choice_name for the given user and return True if decision is reached
        (i.e., vote count for choice exceeds threshold after vote).
        :param user: User casting the vote.
        :param choice_name: Name of choice to vote for.
        '''
        choice = EmuChoice(choice_name)

        if choice.name not in self._choices:
            self._choices.add_choice(choice_name)

        self._choices.remove_vote(user)
        self._choices.add_vote(user, choice.name)
        
        choice = self._choices.get_choice(choice.name)
        exceeded = choice.votes >= self.threshold

        if self._vote:
            self._vote(self)

        if exceeded:
            self._decision(choice)
            self._choices.clear_votes()

        return exceeded

    def remove_vote(self, user):
        '''
        Remove vote and return True on success.
        :param user: User to remove vote for.
        :param choice_name: Name of choice to remove vote for.
        '''
        return self._choices.remove_vote(user)