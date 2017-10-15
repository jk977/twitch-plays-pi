# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/interfaces/validator.py
# Compiled at: 2017-10-14 19:02:53
# Size of source mod 2**32: 376 bytes
from . import *
from interfaces.serializable import Serializable

class Validator(Serializable):
    """
    Base class for serializable classes that can validate inputs by attempting to deserialize them.
    """

    @classmethod
    def validate(cls, message):
        try:
            cls.deserialize(message)
            return True
        except:
            return False