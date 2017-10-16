from interfaces.votemanager import VoteManager
from nes.emuchoice import EmuChoice


class InputManager(VoteManager):
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