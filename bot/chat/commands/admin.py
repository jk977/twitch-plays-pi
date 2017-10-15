# uncompyle6 version 2.13.2
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.5.2 (default, Sep 14 2017, 22:51:06) 
# [GCC 5.4.0 20160609]
# Embedded file name: /home/jk/Desktop/cs/projects/twitch-plays/bot/chat/commands/admin.py
# Compiled at: 2017-10-13 01:01:48
# Size of source mod 2**32: 383 bytes
import sys

def admin_cmd(func):
    """
    Decorator that prevents function execution if message author isn't admin.
    """

    def wrapper(chat, message):
        if message.author.admin:
            return func(chat, message)

    return wrapper


@admin_cmd
def test_cmd(chat, message):
    return message


@admin_cmd
def restart(chat, message):
    chat.close()
    sys.exit(0)