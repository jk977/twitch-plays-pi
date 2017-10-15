# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/commands/command.py
# Compiled at: 2017-10-14 02:01:42
# Size of source mod 2**32: 282 bytes


class Command:

    def __init__(self, command, kwargs):
        if not callable(command):
            raise TypeError('Command must be callable.')
        self._command = command
        self._kwargs = kwargs

    def run(self):
        return self._command(**self._kwargs)