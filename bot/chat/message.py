import config
import re
from chat.user import User


class Message:
    def __init__(self, raw_message):
        header = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
        name = re.search(r'(\w+)', raw_message).group(0).strip()

        if name not in config.users:
            is_owner = name == config.CHAN
            author = User(name=name, owner=is_owner)
            config.users[name] = author

        self._author = config.users[name]
        self._contents = header.sub('', raw_message).strip()

    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._contents
