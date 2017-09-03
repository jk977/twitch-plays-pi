"""Testing new vote functionality."""
from chat.user import User
from tests.utils import *


# initializing test variables
u1 = User(name='Phil', owner=True)
u2 = User(name='Bob', moderator=True)
u3 = User(name='Steve', moderator=True)
u4 = User(name='Mark')
u5 = User(name='Henry')
users = [u1,u2,u3,u4,u5]


def print_user_roles(user):
    name = user.name
    msg = '{} is {}: {}'
    print(msg.format(name, 'banned', user.is_banned))
    print(msg.format(name, 'mod', user.is_moderator))
    print(msg.format(name, 'owner', user.is_owner))


def print_all_roles():
    print('Roles\n')
    for user in users:
        print_user_roles(user)
        print()
    print('=====================')


def test_roles():
    print_all_roles()
    
    # validating constructor results
    try:
        assert(u1.is_owner)
        assert(u2.is_moderator and u3.is_moderator)
        print('Constructors working correctly')
        print('=====================')
    except AssertionError:
        print('Constructors not working as intended.')
        print_user_roles(u1)
        print_user_roles(u2)
        print_user_roles(u3)
        return False


    # making sure owner can't get banned
    try:
        u1.ban()
        print('Banned owner!')
        print_user_roles(u1)
        return False # owner isn't bannable
    except PermissionError:
        pass


    # testing banning
    try:
        u4.ban()
        assert(u4.is_banned)
        u4.ban()
        assert(u4.is_banned)

        u5.mod()
        u5.ban()
        assert(u5.is_banned)

        print('Banning works correctly.')
        print('=====================')
    except AssertionError:
        print('Error in banning tests.')
        print_user_roles(u4)
        print_user_roles(u5)
        return False


    # testing unbanning
    try:
        u4.unban()
        u5.unban()
        assert(not (u4.is_banned or u5.is_banned))

        u4.unban()
        assert(not u4.is_banned)

        print('Unbanning works correctly.')
        print('=====================')
    except AssertionError:
        print('Error in unbanning tests.\n')
        print_user_roles(u4)
        print_user_roles(u5)
        return False

    print_all_roles()
    return True


if __name__ == '__main__':
    if test_roles():
        print('Test successful!')
    else:
        print('Test failed.')
