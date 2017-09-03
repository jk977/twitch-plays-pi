from tests.testcommandparser import test_command_parser
from tests.testcommands import test_commands
from tests.testvotes import test_votes
from tests.testroles import test_roles
from tests.testthreads import test_threads


def test_all(vote_count=50):
    success = True

    if not test_command_parser():
        print('Command parser test failed.')
        success = False

    if not test_commands():
        print('Command test failed.')
        success = False

    if not test_roles():
        print('Role test failed.')
        success = False

    if not test_threads():
        print('Thread test failed.')
        success = False

    if not test_votes(vote_count): 
        print('Vote test failed.')
        success = False

    return success


if __name__ == '__main__':
    if test_all():
        print('Tests successful!')
    else:
        print('Tests failed.')
