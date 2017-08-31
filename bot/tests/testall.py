from tests.testvotes import test_votes
from tests.testroles import test_roles

def test_all(vote_count, role_count):
    return test_votes(vote_count) and test_roles(role_count)

if __name__ == '__main__':
    if test_all(50, 50):
        print('Tests successful!')
    else:
        print('Tests failed.')
