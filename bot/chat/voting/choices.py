import json

from nes.emuchoice import EmuChoice
from interfaces.serializable import Serializable


class Choices(Serializable):
    def __init__(self, *args):
        """
        Initializes Choices object, which wraps dictionary pairing choice name with EmuChoice object.
        """
        if not all((isinstance(choice, EmuChoice) for choice in args)):
            raise TypeError('Arguments must be EmuChoice objects.')

        choices = set(args)
        self._choices = {}

        for choice in choices:
            self._choices[choice.name] = choice

    def __contains__(self, item):
        return item in self._choices

    def __eq__(self, other):
        return isinstance(other, Choices) and self._choices == other._choices

    def add_choice(self, choice_name):
        """
        Adds choice to list.
        :param choice_name: Name of choice to add.
        """
        choice = EmuChoice(choice_name)
        self._choices[choice.name] = choice
        return True

    def add_vote(self, user, choice_name):
        """
        Adds vote for choice_name by user, and returns True on success.
        :param user: User voting.
        :param choice_name: Name of choice to vote for.
        """
        return self._choices[choice_name].add_vote(user)

    def remove_choice(self, choice_name):
        """
        Removes choice from list.
        :param choice_name: Name of choice to remove.
        """
        if choice_name not in self._choices:
            return False

        self._choices.remove(choice_name)
        return True

    def remove_vote(self, user):
        """
        Removes vote by user.
        :param user: User removing vote.
        """
        for k in self._choices.keys():
            if self._choices[k].remove_vote(user):
                return True

        return False

    def get_choice(self, choice_name):
        """
        Gets specified choice, or returns False.
        :param choice_name: Name of choice to get.
        """
        return self._choices.get(choice_name, False)

    def get_voters(self, choice_name):
        """
        Gets list of voters for specified choice.
        :param choice_name: Name of choice to get voter list for.
        """
        if choice_name not in self._choices:
            return False

        return self._choices[choice_name].voters

    def get_votes(self, choice_name):
        """
        Gets vote count for specified choice.
        :param choice_name: Name of choice to get vote count for.
        """
        if choice_name not in self._choices:
            return False

        return self._choices[choice_name].votes

    def clear_votes(self, hard=False):
        """
        Clears votes for all choices.
        :param hard: If True, removes all choices as well as votes.
        """
        if hard:
            self._choices = {}
        else:
            for name in self._choices:
                self._choices[name].clear()

    def serialize(self):
        fields = [choice.serialize() for choice in self._choices.values()]
        return json.dumps(fields)

    def deserialize(serialized):
        fields = json.loads(serialized)
        fields = [EmuChoice.deserialize(choice) for choice in fields]
        return Choices(*fields)