import config
import json
import os

from chat.roles import Roles
from chat.user import User


class Settings:
    """
    Saves and loads settings from a file to carry between seessions.
    """
    default_path = 'info/settings.json'


    def save_settings(destination=None):
        if not destination:
            destination = Settings.default_path

        settings = {'users': {}}

        if not config.users:
            print('No users found.')
            return

        for user in config.users.values():
            user_settings = {'role': None}
            user_settings['role'] = user.role
            settings['users'][user.name] = user_settings

        try:
            with open(destination, 'w') as file:
                json.dump(settings, file)
        except:
            print('Failed to save settings.')


    def load_settings(source=None):
        if not source:
            source = Settings.default_path

        file_valid = True

        try:
            with open(source, 'r') as file:
                settings = json.load(file)

        except FileNotFoundError:
            file_valid = False

        if not file_valid:
            try:
                os.remove(source)
                print('Configuration file isn\'t valid. Removed file.')
            except PermissionError:
                print('Configuration file cannot be read.')
            except FileNotFoundError:
                print('Configuration file does not exist.')

        else:
            users = settings.get('users', None)

            if not users:
                print('Failed to retrieve user list.')
                return

            for name, user in users.items():
                role = user['role']
                mod = role & Roles.MOD
                banned = role & Roles.BANNED
                owner = role & Roles.OWNER

                user_obj = User(name=name, banned=banned, moderator=mod, owner=owner)
                config.users[name] = user_obj
