import config
import re
from chat.user import User


class Message:
    def __init__(self, raw_message):
        header = re.compile(r'^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :')
        self._author = re.search(r'(\w+)', raw_message).group(0).strip()
        self._contents = header.sub('', raw_message).strip()


    @property
    def author(self):
        return self._author

    @property
    def content(self):
        return self._contents
