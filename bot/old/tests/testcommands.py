from chat.commands import Command


def foo(**kwargs):
    args = kwargs.get('args', None)

    if args:
        args = [str(arg) for arg in args]
        print('arguments: {}'.format(', '.join(args)))
    else:
        print('args is empty')


# initializing test variables
cmd1 = Command(action=foo)
cmd2 = Command(action=foo, args=(1,))
cmd3 = Command(action=foo, args=(1,2,'bar'))


def test_commands():
    try:
        cmd1.run()
        print('First command passed.')
        cmd2.run()
        print('Second command passed.')
        cmd3.run()
        print('Third command passed.')
    except TypeError as e:
        print(e)
        return False

    return True


if __name__ == '__main__':
    if test_commands():
        print('Test successful!')
    else:
        print('Test failed.')
