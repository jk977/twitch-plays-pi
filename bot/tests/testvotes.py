"""Testing new vote functionality."""
import itertools

from user import User
from votes.votemanager import VoteManager
from tests.utils import *


# initializing test variables
v = VoteManager(threshold=3)
u1 = User(name='Phil')
u2 = User(name='Bob')
u3 = User(name='Steve')
u4 = User(name='Mark')
u5 = User(name='Henry')
users = [u1,u2,u3,u4,u5]

buttons = ['1start', '9A', '4up', '6select', '2right', '6B']
cheats = ['foo', 'bar', 'baz']
scores = dict(zip(buttons+cheats, itertools.repeat(0)))


def print_all_votes():
    print('Votes\n')
    for user in users:
        if user.choice is None:
            continue
        print(user.name + ': ' + user.choice)
    if v.vote_total() == 0:
        print('No votes')
    print('----------------------')


def vote_and_print(user, choice):
    try:
        result = user.vote(v, choice)
        print(user.name + ' cast vote for ' + choice)
        print(choice + ' total: ' + str(result))
    except ValueError:
        print('Bad input')

    print('----------------------')
    return result


def test_votes(test_count):
    print_all_votes()

    for i in range(test_count):
        user = pick_random_element(users)
        vote_is_button = bool(randint(0,1))

        if vote_is_button:
            choice = pick_random_element(buttons)
        else:
            choice = pick_random_element(cheats)

        scores[choice] += 1
        if user.choice:
            scores[user.choice] -= 1

        result = vote_and_print(user, choice)

        try:
            assert(v.vote_total() <= len(users))
            assert(scores[choice] == result)
        except AssertionError:
            print_all_votes()
            print('Debug info\n')
            print('User: ' + user.name)
            print('User vote: ' + user.choice)
            print('Choice: ' + choice)
            print('Choice is user vote: ' + str(user.choice == choice))
            print('Number of recorded votes: ' + str(votes_stored))
            print('Total number of votes cast: ' + str(i+1))
            print('Total users: ' + str(len(users)))
            return False

        if (i+1)%10 == 0:
            print_all_votes()

    return True


if __name__ == '__main__':
    if test_votes(50):
        print('Test successful!')
    else:
        print('Test failed.')
