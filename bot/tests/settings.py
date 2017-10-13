import config
import json
import os
import unittest

from chat.user import User
from settings import Settings

class TestSettings(unittest.TestCase):
    def test_save(self):
        Settings.save()
        path = os.path.join(config.info_dir, Settings.destination)
        
        with open(path, 'r') as file:
            other = json.loads(file.read().strip())

        self.assertIsNotNone(other['users'], 'Settings save failed')

    def test_load(self):
        u1 = 'bob'
        u2 = 'steve'
        u3 = 'bill'
        config.users = { u1: User(u1), u2: User(u2) }
        Settings.save()

        config.users[u3] = User(u3)
        users = config.users
        Settings.load()
        
        self.assertNotEqual(users, config.users, 'Settings load failed')