# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/interfaces/chat.py
# Compiled at: 2017-10-11 17:38:50
# Size of source mod 2**32: 285 bytes
from . import *

class Chat(ABC):
    """
    Interface for sending and receiving messages.
    """

    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def get_message(self):
        pass

    @abstractmethod
    def close(self):
        pass