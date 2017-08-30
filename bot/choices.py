# TODO redo voting system (again)?
# Seems flipped - instead of calling choice.vote(user) to vote,
# user.vote(choice) should be called
import re
from choice import Choice

class Choices():
    def __init__(self, choices=[], choice_format='', threshold=1):
        self._choices = set(choices)
        self._format = re.compile(choice_format)
        self._threshold = threshold

    def __find_choice(self, name):
        for choice in self._choices:
            if name == choice.name:
                return choice

    def __update_choices(self):
        self._choices = set([choice for choice in self._choices if choice.count() > 0])

    @property
    def threshold(self):
        return self._threshold

    @property
    def votes(self):
        """Returns dict matching votes to voters"""
        output = {}
        for choice in self._choices:
            output[choice.name] = choice.voters
        return output

    def vote_count(self, choice):
        """Returns number of votes for specified choice"""
        return self.__find_choice(choice).count()

    def clear(self):
        """Removes all voting info"""
        self._choices = set()

    def rm_user_votes(self, user):
        for choice in self._choices:
            self.unvote(user, choice.name)

    def vote(self, user, choice_name):
        if not self._format.match(choice_name):
            return

        self.rm_user_votes(user)
        choice = self.__find_choice(choice_name)

        if choice:
            choice.vote(user)
        else:
            choice = Choice(name=choice_name, voters=[user])
            self._choices.add(choice)

    def unvote(self, user, choice_name):
        choice = self.__find_choice(choice_name)

        if choice:
            choice.unvote(user)
            self.__update_choices()
