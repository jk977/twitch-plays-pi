"""Testing new vote functionality."""
from choices import Choices

c = Choices(choice_format=r'^[1-9]\w+$', threshold=1)

def do(callback, *args):
    callback(*args)
    results = c.votes

    for vote in results:
        print(vote + ':', results[vote])

    if len(results) == 0:
        print('No votes')

    print('-----------')

do(c.vote, 'bob', '1A')
do(c.vote, 'phil', '9start')
do(c.vote, 'bob', '3B')
do(c.clear)
do(c.vote, 'steve', '6up')
do(c.vote, 'mark', 'not an input')
do(c.vote, 'henry', '1left')
do(c.vote, 'bill', '1left')
do(c.vote, 'fred', '1left')
do(c.vote, 'steve', '1left')
