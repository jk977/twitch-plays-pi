# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/settings.py
# Compiled at: 2017-10-13 03:59:26
# Size of source mod 2**32: 784 bytes
import config
import json
import os
from chat.user import User

class Settings:
    destination = 'settings.json'

    def save(path=None):
        if not path:
            path = os.path.join(config.info_dir, Settings.destination)
        fields = {'users': [u.serialize() for u in config.users.values()]}
        ser = json.dumps(fields)
        with open(path, 'w') as file:
            file.write(ser)

    def load(path=None):
        if not path:
            path = os.path.join(config.info_dir, Settings.destination)
        with open(path, 'r') as file:
            ser = file.read().strip()
        fields = json.loads(ser)
        config.users = {}
        for ser in fields['users']:
            user = User.deserialize(ser)
            config.users[user.name] = user