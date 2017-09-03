# TODO fix test
import traceback

from chat.commandparser import CommandParser
from chat.user import User


# initializing test variables
m1 = '!ban bob'
m2 = '!unban bob'
m3 = '!help'
m4 = '!game wrong'
m5 = '!game killall'
m6 = '!banlist'
m7 = '!restart'
m8 = 'not a command'
  
messages = [m1,m2,m3,m4,m5,m6,m7]

u1 = User(name='Phil', owner=True)
u2 = User(name='Bob', moderator=True)
u3 = User(name='Steve', moderator=True)
u4 = User(name='Mark')
u5 = User(name='Henry')
users = [u1,u2,u3,u4,u5]

u5.ban()

sock = 'dummy'
valid_commands = []
invalid_commands = []


def parse(message, user):
    print('Parsing {} from {}...'.format(message, user.name))
    cmd = CommandParser.parse(message, user, sock)
    print('Command parsed!\n')

    return cmd


def test_command_parser():
    # TODO find out why permission-related commands work in a test environment,
    # but do in the actual bot
    try:
        cmd1 = parse(m1,u1)
        cmd2 = parse(m2,u2)
        cmd3 = parse(m3,u3)
        cmd4 = parse(m8,u4)

        valid_commands = [cmd for cmd in [cmd1, cmd2, cmd3, cmd4] if cmd is not None]
    except PermissionError as e:
        print(e)
    except Exception:
        print('Parsing commands failed.')
        return False

    try:
        assert(len(valid_commands) == 3)
        print('Commands parsed as expected\n')
    except AssertionError:
        print('Expected 3 commands after first batch but got {}.'.format(len(valid_commands)))
        return False

    return True


if __name__ == '__main__':
    if test_command_parser():
        print('Test passed!')
    else:
        print('Test failed.')
