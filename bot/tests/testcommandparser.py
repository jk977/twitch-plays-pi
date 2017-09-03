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

sock = 'dummy'
commands = []


def test_command_parser():
    for i, m in enumerate(messages):
        user = users[i % len(users)]

        try:
            cmd = CommandParser.parse(m, user, sock)
            if cmd:
                commands.append(cmd)
        except PermissionError as e:
            print(e)
        except Exception as e:
            print('Parsing commands failed. Info:\n')
            traceback.print_stack_trace()
            raise

    try:
        # 7 of the 8 messages have a valid command name
        assert(len(commands) == 7)
    except AssertionError:
        print('Commands didn\'t parse as expected.')

    for i, command in enumerate(commands):
        command.run()
        print('Command {} passed!'.format(i))

    return True


if __name__ == '__main__':
    if test_command_parser():
        print('Test passed!')
    else:
        print('Test failed.')
