"""Testing new vote functionality."""
import itertools

from user import User
from tests.utils import *

# initializing test variables
u1 = User(name='Phil')
u2 = User(name='Bob')
u3 = User(name='Steve')
u4 = User(name='Mark')
u5 = User(name='Henry')
users = [u1,u2,u3,u4,u5]

roles = ['foo', 'bar', 'baz']
role_log = dict(zip([user.name for user in users], itertools.repeat(None)))

for user in role_log:
    role_log[user] = set()


def print_all_roles():
    print('Roles\n')
    for user in users:
        if user.roles == []:
            continue
        print(user.name + ': ' + str(user.roles))

    if not [user for user in users if len(user.roles) != 0]:
        print('No roles assigned.')
    print('----------------------')


def add_and_print(user, role):
    user.add_role(role)
    print('Added ' + role + ' to ' + user.name)
    print(user.name + ' roles: ' + str(user.roles))
    print('----------------------')


def remove_and_print(user, role):
    user.remove_role(role)
    print('Removed ' + role + ' from ' + user.name)
    print(user.name + ' roles: ' + str(user.roles))
    print('----------------------')


def test_roles(test_count):
    print_all_roles()

    for i in range(test_count):
        user = pick_random_element(users)
        role = pick_random_element(roles)
        role_added = bool(randint(0,1))

        if role_added:
            add_and_print(user, role)
            role_log[user.name].add(role)
        else:
            remove_and_print(user, role)

            try:
                role_log[user.name].remove(role)
            except:
                pass

        try:
            assert(sorted(list(role_log[user.name])) == sorted(user.roles))
        except AssertionError:
            print_all_roles()
            print('Debug info\n')
            print('User: ' + user.name)
            print('Perceived user roles: ' + str(user.roles))
            print('Actual user roles: ' + str(role_log[user.name]))
            print('Number of role changes: ' + str(i+1))
            return False

        if (i+1)%10 == 0:
            print_all_roles()

    return True


if __name__ == '__main__':
    if test_roles(50):
        print('Test successful!')
    else:
        print('Test failed.')
