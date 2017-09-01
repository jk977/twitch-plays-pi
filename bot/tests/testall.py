from tests.testvotes import test_votes
from tests.testroles import test_roles
from tests.testthreads import test_threads


def test_all(vote_count, role_count):
    success = True

    if not test_votes(vote_count): 
        print('Vote test failed.')
        success = False

    if not test_roles(role_count):
        print('Role test failed.')
        success = False

    if not test_threads():
        print('Thread test failed.')
        success = False

    return success


if __name__ == '__main__':
    if test_all(50, 50):
        print('Tests successful!')
    else:
        print('Tests failed.')
