# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/interfaces/serializable.py
# Compiled at: 2017-10-11 17:36:29
# Size of source mod 2**32: 232 bytes
from . import *

class Serializable(ABC):
    """
    Interface for serializable classes.
    """

    @abstractmethod
    def serialize(self):
        pass

    @abstractstaticmethod
    def deserialize(serialized):
        pass