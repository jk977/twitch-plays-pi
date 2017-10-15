import config
import json
import os
import unittest

from chat.user import User
from settings import Settings


def backup_settings():
    path = os.path.join(config.info_dir, Settings.destination)
    with open(path, 'r') as file:
        backup = file.read().strip()
    return backup


def load_backup(backup):
    path = os.path.join(config.info_dir, Settings.destination)
    with open(path, 'w') as file:
        file.write(backup)


def preserve_settings(func):
    def wrapper(*args):
        backup = backup_settings()
        func(*args)
        load_backup(backup)

    return wrapper


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.path = os.path.join(config.info_dir, Settings.destination)

    @preserve_settings
    def test_save(self):
        Settings.save()

        with open(self.path, 'r') as file:
            other = json.loads(file.read().strip())

        self.assertIsNotNone(other['users'], 'Settings save failed')

    @preserve_settings
    def test_load(self):
        u1 = 'bob'
        u2 = 'steve'
        u3 = 'bill'

        config.users = {u1: User(u1), u2: User(u2)}
        Settings.save()

        config.users[u3] = User(u3)
        users = config.users
        Settings.load()

        self.assertNotEqual(users, config.users, 'Settings load failed')